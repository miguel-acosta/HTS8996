import os, re, PyPDF2,csv, sys
import pandas as pd
import numpy as np
import tabula



indir  = '../HTS8996/pdf/' 
outdir = '../HTS8996/csv/'

# These should both be strings, e.g., "1989" and "1"
year   = sys.argv[1]
ch     = sys.argv[2]
files = [year[2:] + '0c' + ch.rjust(2,'0')]

columns = [46+cc for cc in [42,70,288,332,395,474]]
columns = [46+cc for cc in [42,70,288,332,396,474]]
area    = [0,46,1000,1000]
#area    = [78,46,628,1000]

for fname in files: 
    print(fname)
    npages = len(PyPDF2.PdfReader(open(os.path.join(indir,year,fname+'.pdf'),'rb')).pages)
    pages = []
    
    for pp in range(npages): 
        print(pp+1)
        df = tabula.read_pdf(os.path.join(indir,year,fname+'.pdf'),pages=pp+1,
                             pandas_options={'header': None},guess=True,
                             area=area,columns=columns)

        
        if df and df[0].shape[1] >= 7: 
            df = df[0]
            nc = df.shape[1]
            ## Figure out which columns we want
            HTSidx  = 0
            MFNidx  = 4
            UNITidx = 3
            COL2idx = 6

            # Remove footnotes from end of line
            df.loc[:,MFNidx]  = [re.sub('(?:(^|\s)(?:[l0-9]{1}/)+)+$','',str(tt)) if str(tt) != 'nan'
                                 else '' for tt in df.loc[:,MFNidx] ]
            df.loc[:,COL2idx] = [re.sub('(?:(^|\s)(?:[l0-9]{1}/)+)+$','',str(tt)) if str(tt) != 'nan'
                                 else '' for tt in df.loc[:,COL2idx]]

            # Specific tariffs set on items with cubed meters (m^3) as the quantity
            # sometimes have the 3 moved to the front of the tariff rate. These lines
            # of code remove the leading 3 whenever the unit of quantity is m3.
            # (there are also squared-meters--this deals with that too)
            # Mostly these lines end with an "m", but there are a couple of special
            # cases that end with "m +" or "m of"
            # added "not tt.find('.')" for 3.3c/m^2

            df.loc[:,MFNidx]  = [re.sub('^(3|2)','',tt) if len(re.findall('/m[ \+of]*$',tt))>0
                                 and not tt.find('.')==1
                                 else tt for tt  in df.loc[:,MFNidx]]
            df.loc[:,COL2idx]  = [re.sub('^(3|2)','',tt) if len(re.findall('/m[ \+of]*$',tt))>0
                                  and not tt.find('.')==1
                                 else tt for tt in df.loc[:,COL2idx]]
 

            # sometimes "1" get's transcribed as an "l"
            df.loc[:,HTSidx] = [str(hs).replace('l','1') for hs in df.loc[:,HTSidx]]
            
            # Drop rows that are footnotes
            fn = [rr for rr in range(df.shape[0]) if df.loc[rr,HTSidx].strip().find('1/')==0]
            
            if len(fn)>0:
                df.loc[:,'post_footnote'] = [rr>(fn[0]-1) for rr in range(df.shape[0])]
                #df = df.loc[0:(fn[0]-1),:]
            else:
                df.loc[:,'post_footnote'] = 0

            # Get only rows with HS8
            possible_hts = [re.findall('[0-9]{4}\.[0-9]{2}\.[0-9]{2}',str(hh)[0:10])
                            for hh in list(df.loc[:,HTSidx])]
            df.loc[:,HTSidx] = [np.nan if len(ph)==0 else ph[0] for ph in possible_hts]
            # Don't want to ffill past a footnote--put "FN" in the row w/ the first footnote to avoid this 
            if len(fn)>0: 
                df.loc[fn[0],HTSidx]='FN'
            df.loc[:,HTSidx] = df.loc[:,HTSidx].ffill()

            df = df.loc[df.loc[:,HTSidx].isnull()==False,:]

            if df.shape[0]>0 and df.shape[1]>=3: 
            
                # Collapse 
                df.loc[df.loc[:,MFNidx].isnull(),MFNidx] = ''
                df.loc[df.loc[:,COL2idx].isnull(),COL2idx] = ''
                #df = df[[HTSidx,MFNidx,COL2idx,'post_footnote']].groupby(HTSidx).agg(''.join).reset_index()
                df = df[[HTSidx,MFNidx,COL2idx,'post_footnote']].groupby(HTSidx).agg({MFNidx:' '.join,COL2idx:' '.join,'post_footnote':max}).reset_index()
                df.columns = ['HTS','MFN','COL2','post_footnote']

                # Drop footnote rows
                df = df.loc[df.HTS!='FN',:]
                
                pages.append(df)

    full = pd.concat(pages)

    # A bit of cleaning 
    if year in ['1993','1994']:
        full.loc[full.HTS=='1507.90.40','MFN'] = '22.5\%'
        full.loc[full.HTS=='1507.90.40','COL2'] = '45\%'
    if year in ['1996']:
        full.loc[full.HTS=='2106.90.87','MFN'] = '32.2 ¢/kg +9.5%'
        
    # Sometimes an HS8 has a lot of HS10s that spill onto
    # different pages. This keeps the first, which also has the
    # tariff rates 
    full = full.loc[full.duplicated(subset=['HTS'],keep='first')==False,:]
    
    full.to_csv(os.path.join(outdir,year,fname+'.csv'),index=False)

