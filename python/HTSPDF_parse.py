import os, re, sys
import pandas as pd
import numpy as np
sys.path.append('../../../../python/')
from parse_tariffs import * 



indir  = '../HTS8996/csv/' 
outdir = '../HTS8996/'

alldf = []
    
for year in ['1989','1991','1992','1993','1994','1995','1996']:
    files = [ff.replace('.csv','') for ff in os.listdir(os.path.join(indir,year))
             if 'csv' in ff
             and not 'c98' in ff
             and not 'c99' in ff]

            
    print(year)
    for ff in files:
        print(ff)
        df = pd.read_csv(os.path.join(indir,year,ff + '.csv'))

        # Keep raw text for later evaluation
        df.loc[:,'MFN_text' ] = df.MFN
        df.loc[:,'COL2_text'] = df.COL2
        
        # Often 'l' was substituted for 1: 
        df.MFN  = [str(tt).replace('l','1') for tt in df.MFN ]
        df.COL2 = [str(tt).replace('l','1') for tt in df.COL2]
        df.MFN  = [str(tt).replace('1iter','l') for tt in df.MFN ]
        df.COL2 = [str(tt).replace('1iter','l') for tt in df.COL2]
        df.MFN  = [str(tt).lower().replace('dutiab1e','dutiable') for tt in df.MFN ]
        df.COL2 = [str(tt).lower().replace('dutiab1e','dutiable') for tt in df.COL2]
        df.MFN  = [str(tt).lower().replace('tota1','total') for tt in df.MFN ]
        df.COL2 = [str(tt).lower().replace('tota1','total') for tt in df.COL2]        

        # per thousand
        df.MFN  = [re.sub('/[\s]*1[\,]*000','/thousand',str(tt)) for tt in df.MFN  ]
        df.COL2 = [re.sub('/[\s]*1[\,]*000','/thousand',str(tt)) for tt in df.COL2 ]


        # A few tariff rates were written with dashes, e.g., 33-1/3%. Replace dashes
        df.MFN  = [str(tt).replace('-',' ') for tt in df.MFN ]
        df.COL2 = [str(tt).replace('-',' ') for tt in df.COL2]

        # Some tariffs are "free, under bond" which is missed by our current tariff-parsing code 
        df.MFN  = [re.sub('free,[\s]*under[\s]*bond','free',str(tt).lower()) for tt in df.MFN ]
        df.COL2 = [re.sub('free,[\s]*under[\s]*bond','free',str(tt).lower()) for tt in df.COL2]

        for ttype in ['MFN','COL2']:
            parseTariff(df, ttype)
            # Some watches have very complicated tariffs. We will set to missing
            watch = [len(re.findall('on[\s]*the',str(tar)))>0 and 'c91' in ff for tar in df[ttype]]
            for vv in ['specific_rate','adval_rate']:
                df.loc[watch,vv] = np.nan
            for vv in ['specific','both','adval','free']:
                df.loc[watch,vv] = False                
            
            # Set tariffs to 0 when we have one--to distinguish from missng rates
            df.loc[df.free,'specific_rate'] = 0.0
            df.loc[df.free,'adval_rate'] = 0.0
            df.loc[(df.adval==True) & (df.specific==False),'specific_rate'] = 0.0
            df.loc[(df.adval==False) & (df.specific==True),'adval_rate'] = 0.0
            
            df.drop(['both','specific','adval','free'],axis=1,inplace=True)
            df.rename({'specific_rate':ttype+'_specific','adval_rate':ttype+'_adval'},
                      axis=1,inplace=True)
            
        df.drop(['MFN','COL2'],inplace=True,axis=1)
        df.loc[:,'year'] = int(year)
        alldf.append(df)

tariff_year = pd.concat(alldf)
tariff_year = tariff_year[['year','HTS','MFN_adval','MFN_specific','COL2_adval','COL2_specific','MFN_text','COL2_text']]

## Import manual corrections 
corrections = pd.read_excel('../HTS8996/corrections.xlsx')

## Merge corrections on to the OCR version 
corrections.set_index(['HTS', 'year'], inplace=True)
tariff_year.set_index(['HTS', 'year'], inplace=True)
tariff_year.update(corrections, overwrite=True)
tariff_year = pd.concat([corrections.loc[~corrections.index.isin(tariff_year.index),:],tariff_year])
tariff_year.reset_index(inplace=True)

## Set rates to missing when there are "special" rates
tariff_year.loc[:,'special_rate'] = [len(re.findall('rate|see|dutiable',str(tt).lower()))>0
                                     for tt in tariff_year.MFN_text]
for vv in ['MFN_adval','MFN_specific','COL2_adval','COL2_specific']:
    tariff_year.loc[tariff_year.special_rate,vv] = np.nan


## Drop chapters 91, 98, and 99
tariff_year = tariff_year.loc[tariff_year.HTS.str.slice(stop=2).isin(['91','98','99'])==False,:]

## Saving 
tariff_year.sort_values(['HTS','year'],inplace=True)
tariff_year.to_csv(outdir + 'HTS8996.csv',index=False)
