import pandas as pd
import torch as tc

class GrafoBrasilCovid():
    
    def __init__(self, path='dados/gerado/'):
        self.path = path
        self.isLoaded = False
        self.importAll()
    
    def importAll(self):
        self.importMetadata()
        self.importVertices()
        self.importEdges()
        self.isLoaded = True
    
    def freeSpace(self):
        del self.vertex_attr
        del self.vertex_tseries
        del self.edge_index
        self.isLoaded = False
    
    def importMetadata(self):
        df = pd.read_csv(self.path + 'atrib_extra.csv')
        self.graph_info = {
            'populacao': int (df[ df['atrib']=='populacao' ]['valor'].values),
            'municipios': int (df[ df['atrib']=='municipios' ]['valor'].values),
            'dias': int (df[ df['atrib']=='dias' ]['valor'].values),
            'casos': int (df[ df['atrib']=='casos' ]['valor'].values),
            'mortes': int (df[ df['atrib']=='mortes' ]['valor'].values),
            
            'data_inicio': str (df[ df['atrib']=='data_inicio' ]['valor'].values[0]),
            'data_termino': str (df[ df['atrib']=='data_termino' ]['valor'].values[0]),
            
            'con_aer': int (df[ df['atrib']=='con_aer' ]['valor'].values),
            'con_fer': int (df[ df['atrib']=='con_fer' ]['valor'].values),
            'con_hid': int (df[ df['atrib']=='con_hid' ]['valor'].values),
            'con_rod': int (df[ df['atrib']=='con_rod' ]['valor'].values),
            'con_fro': int (df[ df['atrib']=='con_fro' ]['valor'].values)
        }
    
    def importVertices(self):
        # atributos estáticos dos municípios, indexado sequencialmente e por unidade federativa
        df = pd.read_csv(self.path + 'atrib_estat.csv')
        df.drop(columns=['perimetro'], inplace=True)
        self.vertex_attr = df.to_dict('records')
        self.geocode_list = df['geocodigo']
        self.geocode_index = {gcode: i for i, gcode in enumerate(self.geocode_list)}
        self.regional_index = {}
        
        for uf in df['estado'].unique():
            self.regional_index[uf] = df[ df['estado']==uf ].index.values
        
        #  tensor de série temporal com 2 atributos por municipio e dia: num. casos e num. mortes
        df = pd.read_csv(self.path + 'atrib_dinam.csv')
        df.sort_values(by=['dia','geocodigo'], inplace=True)
        cols = ['casos', 'mortes']
        dias = self.graph_info['dias']
        self.vertex_tseries = tc.cat([ 
            tc.tensor([df[ df['dia']==i+1 ][cols].values], dtype=tc.float) for i in range(dias)
        ])

        self.graph_info['qt_uf'] = len(self.regional_index)
        self.graph_info['dim_estat'] = 3 # população, leitos hospitalares e área territorial
        self.graph_info['dim_dinam'] = 2 # número de casos e mortes
    
    def importEdges(self):
        df = pd.read_csv(self.path + 'lista_rel.csv')
        f = lambda x: self.geocode_index[ x ]

        # arestas no sentido oposto
        # (desnecessário com o módulo utilizado)
        #mirror = pd.DataFrame(index=df.index, data={
        #    'geocodigo_1': df['geocodigo_2'].values,
        #    'geocodigo_2': df['geocodigo_1'].values,
        #})
        #mirror = mirror.merge(df[['distancia', 'AER', 'FER', 'HID', 'ROD', 'FRO']], 
        #                      left_index=True, right_index=True)
        #df = df.append(mirror, ignore_index=True).drop_duplicates()

        self.graph_info['malhas'] = list (df.columns[3:])
        self.edge_index = tc.tensor([df['geocodigo_1'].apply(f).values, 
                                     df['geocodigo_2'].apply(f).values], dtype=tc.long)
        self.edge_mask = {tag: df[tag].values for tag in self.graph_info['malhas']}
        self.edge_dist = tc.tensor(df['distancia'].values)
