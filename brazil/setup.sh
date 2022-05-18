#wget -P data/IBGE/LogisticaTransporte/ https://www.ibge.gov.br/geociencias/cartas-e-mapas/redes-geograficas/15793-logistica-dos-transportes.html?=&t=downloads

#phantomjs /aux/ibge_logtransp_click_trigger.js "https://www.ibge.gov.br/geociencias/cartas-e-mapas/redes-geograficas/15793-logistica-dos-transportes.html?=&t=downloads" > "data/IBGE/LogisticaTransporte/2014.zip"
  
echo -e "Download IBGE's \"Logistica de Transporte\" dataset at https://www.ibge.gov.br/geociencias/cartas-e-mapas/redes-geograficas/15793-logistica-dos-transportes.html?=&t=downloads > base_de_dados > 2014.zip \n" 
