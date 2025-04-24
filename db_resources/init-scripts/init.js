// Load data from JSON files

const local_path = '/docker-entrypoint-initdb.d';
const school = 'ET';

const disciplinas = require(`${local_path}/disciplinas.${school}.json`);
const escola = require(`${local_path}/escolas.${school}.json`);
const fs = require('fs');

const titleToAreaMap = require(`${local_path}/titleToAreaMap`);
const competenciasMatriz = require(`${local_path}/matriz_competencias.json`)

// Create a map for cognitive skills
const keyToTitleCognitivos = new Map([
    ['DL', 'Dominar Linguagens'],
    ['CF', 'Compreender Fenômenos'],
    ['SP', 'Situações Problema'],
    ['CA', 'Construir argumentação'],
    ['EP', 'Elaborar Propostas']
])

// Select the database
db = db.getSiblingDB("competencias_enem_data")

// Insert the competencies into the database
const matrizData = []


Object.entries(competenciasMatriz['COMPETENCIAS_EIXOS_COGNITIVOS']).forEach(([key, value]) => {
    matrizData.push({
        nome: keyToTitleCognitivos.get(key),
        tag: 'COGNITIVOS',
        descricao: value,
    })
})

competenciasMatriz['MATRIZES_REFERENCIA_POR_AREA'].forEach((matrizArea) => {
    matrizArea['competencias_especificas'].forEach(competencia => {
        const { competencias, descricao_area } = competencia
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

// Create Series Array
const series = ["1º ano", "2º ano", "3º ano"];
const novas_turmas = [];

// Generate new ID for the school
escola._id = ObjectId();

// Add disciplines to school with new IDs
escola.disciplinas = disciplinas.map(disciplina => ({
    ...disciplina,
    _id: ObjectId()
}));

// Process classes
const historicos = {};

escola.turmas.forEach(turma => {
    series.forEach(serie => {
        const nova_turma = JSON.parse(JSON.stringify(turma));
        nova_turma.serie = serie;
        nova_turma._id = new ObjectId();
        const serie_num = parseInt(serie[0]);
        nova_turma.ano = nova_turma.ano + serie_num - 1;

        // Filter disciplines by grade
        const disciplinas_from_serie = escola.disciplinas.filter(
            d => d.serie_ano === serie_num
        );

        // Create history records
        historicos[serie] = disciplinas_from_serie.map(d => ({
            disciplina_id: d._id.toString(),
            disciplina_titulo: `${d.nome}-${d.serie_ano}`,
            nota: 0
        }));

        novas_turmas.push(nova_turma);
    });
});

// Update school with processed classes
escola.turmas = novas_turmas;

db.escolas.insertOne(escola);

const outputPath = `tmp/historico.${school}.json`;
fs.writeFileSync(outputPath, JSON.stringify(historicos, null, 2));
