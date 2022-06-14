TARGET=$PWD/dados/fonte/

echo -e "\nDownload das séries históricas de casos e mortes\n\t- fonte: Brasil.io\n"
mkdir -p $TARGET/Brasil.io/ 
wget -P $TARGET/Brasil.io/ https://data.brasil.io/dataset/covid19/caso_full.csv.gz
gzip -d $TARGET/Brasil.io/*.gz


echo -e "\nDownload de dados de logística de transporte\n\t- fonte: IBGE\n"
mkdir -p $TARGET/IBGE_LogTransp/
python3 aux/get_ibge_dataset_logtransp.py
unzip $TARGET/IBGE_LogTransp/*.zip -d $TARGET/IBGE_LogTransp/
rm $TARGET/IBGE_LogTransp/*.zip 


echo -e "\nDownload de dados de bases cartográficas\n\t- fonte: IBGE\n"
mkdir -p $TARGET/IBGE_BasesCart/
python3 aux/get_ibge_dataset_basescart.py
unzip $TARGET/IBGE_BasesCart/*.zip -d $TARGET/IBGE_BasesCart/shapefile_2019
rm $TARGET/IBGE_BasesCart/*.zip 
