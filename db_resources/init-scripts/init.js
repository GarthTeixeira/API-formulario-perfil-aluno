const titleToAreaMap = require('/docker-entrypoint-initdb.d/titleToAreaMap');  // Use require apenas se necessário

const competenciasMatriz = require('/docker-entrypoint-initdb.d/matriz_competencias.json')

const keyToTitleCognitivos =  new Map([
    ['DL', 'Dominar Linguagens'],
    ['CF', 'Compreender Fenômenos'],
    ['SP', 'Situações Problema'],
    ['CA', 'Construir argumentação'],
    ['EP', 'Elaborar Propostas']
])

db = db.getSiblingDB("competencias_enem_data")

const matrizData = []


Object.entries(competenciasMatriz['COMPETENCIAS_EIXOS_COGNITIVOS']).forEach(([key, value])=>{
    matrizData.push({
        nome: keyToTitleCognitivos.get(key),
        tag: 'COGNITIVOS',
        descricao:value,
    })
})

competenciasMatriz['MATRIZES_REFERENCIA_POR_AREA'].forEach((matrizArea)=>{
    matrizArea['competencias_especificas'].forEach(competencia=>{
        const { competencias, descricao_area} = competencia
        matrizData.push(
            {
                descricao_area,
                competencias_habilidades: competencias,
                tag: titleToAreaMap.get(matrizArea['nome_matriz'])
            }
        )
    })
})

db.competencias.insertMany(matrizData)