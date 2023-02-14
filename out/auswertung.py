from sys import displayhook
import pandas as pd
import regex as re
base='/Users/christine/Documents/education/university/Praxisarbeit/PA2/PA2-Code/May2019_sent-bias/csv-tsv'

df_orig = pd.read_csv(base+'/results-May.csv', sep=",", names=['options', 'test', 'p_value', 'effect_size'])
df_en = pd.read_csv(base+'/en-test.csv', sep=",", names=['options', 'test', 'p_value', 'effect_size'])
df_de = pd.read_csv(base+'/german-bert-original.csv', sep=",", names=['options', 'test', 'p_value', 'effect_size'])
df_dbmdz = pd.read_csv(base+'/german-bert-dbmdz.csv', sep=",", names=['options', 'test', 'p_value', 'effect_size'])
df_geo = pd.read_csv(base+'/german-bert-geotrend.csv', sep=",", names=['options', 'test', 'p_value', 'effect_size'])

df_orig = df_orig[df_orig['options']=='version=bert-base-cased*']

df_orig.sort_values(by = 'test', inplace=True)
df_en.sort_values(by = 'test',inplace=True)
df_de.sort_values(by = 'test',inplace=True)
df_dbmdz.sort_values(by = 'test',inplace=True)
df_geo.sort_values(by = 'test',inplace=True)


df_orig.p_value.astype(float)
df_en.p_value.astype(float)
df_de.p_value.astype(float)
df_dbmdz.p_value.astype(float)
df_geo.p_value.astype(float)


difference = pd.DataFrame()
difference['test'] = df_orig['test']

difference['p-val_de-geo'] = abs(df_de['p_value'].astype(float) - df_geo['p_value'].astype(float))
difference['p-val_de-dbmdz'] = abs(df_de['p_value'].astype(float) - df_dbmdz['p_value'].astype(float))
difference['p-val_geo-dbmdz'] = abs(df_geo['p_value'].astype(float) - df_dbmdz['p_value'].astype(float))
difference['p-val_de-en'] = abs(df_de['p_value'].astype(float) - df_en['p_value'].astype(float))
difference['p-val_geo-en'] = abs(df_geo['p_value'].astype(float) - df_en['p_value'].astype(float))
difference['p-val_dbmdz-en'] = abs(df_dbmdz['p_value'].astype(float) - df_en['p_value'].astype(float))

difference['effect_de-geo'] = abs(df_de['effect_size'].astype(float) - df_geo['effect_size'].astype(float))
difference['effect_de-dbmdz'] = abs(df_de['effect_size'].astype(float) - df_dbmdz['effect_size'].astype(float))
difference['effect_geo-dbmdz'] = abs(df_geo['effect_size'].astype(float) - df_dbmdz['effect_size'].astype(float))
difference['effect_de-en'] = abs(df_de['effect_size'].astype(float) - df_en['effect_size'].astype(float))
difference['effect_geo-en'] = abs(df_geo['effect_size'].astype(float) - df_en['effect_size'].astype(float))
difference['effect_dbmdz-en'] = abs(df_dbmdz['effect_size'].astype(float) - df_en['effect_size'].astype(float)
)
difference['effect_orig-de'] = abs(df_orig['effect_size'].astype(float) - df_de['effect_size'].astype(float))
difference['effect_orig-en'] = abs(df_orig['effect_size'].astype(float) - df_en['effect_size'].astype(float))
difference['effect_orig-dbmdz'] = abs(df_orig['effect_size'].astype(float) - df_dbmdz['effect_size'].astype(float))
difference['effect_orig-geo'] = abs(df_orig['effect_size'].astype(float) - df_geo['effect_size'].astype(float))
difference['p-val_orig-de'] = abs(df_orig['p_value'].astype(float) - df_de['p_value'].astype(float))
difference['p-val_orig-en'] = abs(df_orig['p_value'].astype(float) - df_en['p_value'].astype(float))
difference['p-val_orig-dbmdz'] = abs(df_orig['p_value'].astype(float) - df_dbmdz['p_value'].astype(float))
difference['p-val_orig-geo'] = abs(df_orig['p_value'].astype(float) - df_geo['p_value'].astype(float))

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(difference)

print('p_val')
print('de-geo',difference['p-val_de-geo'].describe())
print('de-dbmdz',difference['p-val_de-dbmdz'].describe())
print('de-en',difference['p-val_de-en'].describe())
print('orig-de',difference['p-val_orig-de'].describe())

print('effect_size')
print('de-geo',difference['effect_de-geo'].describe())
print('de-dbmdz',difference['effect_de-dbmdz'].describe())
print('de-en',difference['effect_de-en'].describe())
print('orig-de',difference['effect_orig-de'].describe())

print('(------)')
print(difference['p-val_de-geo'].median())
print(difference['p-val_de-dbmdz'].median())
print(difference['p-val_geo-dbmdz'].median())
print(difference['p-val_de-en'].median())
print(difference['p-val_geo-en'].median())
print(difference['p-val_dbmdz-en'].median())
print(difference['p-val_orig-en'].median())
print(difference['p-val_orig-de'].median())
print(difference['p-val_orig-dbmdz'].median())
print(difference['p-val_orig-geo'].median())
print('ORIGINAL-p')
print(difference['p-val_orig-de'].median())
print(difference['p-val_orig-en'].median())
print(difference['p-val_orig-dbmdz'].median())
print(difference['p-val_orig-geo'].median())
print('effect')
print(difference['effect_de-geo'].median())
print(difference['effect_geo-dbmdz'].median())
print(difference['effect_de-en'].median())
print(difference['effect_geo-en'].median())
print(difference['effect_dbmdz-en'].median())
print('ORIGINAL-effect')
print(difference['effect_orig-de'].median())
print(difference['effect_orig-en'].median())
print(difference['effect_orig-dbmdz'].median())
print(difference['effect_orig-geo'].median())
print('(------)')
print(difference['p-val_de-geo'].mean())
print(difference['p-val_de-dbmdz'].mean())
print(difference['p-val_geo-dbmdz'].mean())
print(difference['p-val_de-en'].mean())
print(difference['p-val_geo-en'].mean())
print(difference['p-val_dbmdz-en'].mean())
print('ORIGINAL-p')
print(difference['p-val_orig-de'].mean())
print(difference['p-val_orig-en'].mean())
print(difference['p-val_orig-dbmdz'].mean())
print(difference['p-val_orig-geo'].mean())
print('effect')
print(difference['effect_de-geo'].mean())
print(difference['effect_geo-dbmdz'].mean())
print(difference['effect_de-en'].mean())
print(difference['effect_geo-en'].mean())
print(difference['effect_dbmdz-en'].mean())
print('ORIGINAL-effect')
print(difference['effect_orig-de'].mean())
print(difference['effect_orig-en'].mean())
print(difference['effect_orig-dbmdz'].mean())
print(difference['effect_orig-geo'].mean())
