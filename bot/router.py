import os
import logging
from typing import List

logger = logging.getLogger(__name__)

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "knowledge")

# Base geral de conhecimento — sempre incluída em toda resposta
GENERAL_KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "knowledge.txt")

# Sempre incluído em toda resposta — fundamentos do curso
BASE_FILES = ["00_principios_gerais.txt"]

TOPICS = [
    {
        "id": "captacao",
        "file": "01_captacao.txt",
        "keywords": [
            "captação", "captar", "lead", "prospecção", "lista fria",
            "facebook orgânico", "tráfego pago", "anúncio", "marketplace",
            "porteiro", "zelador", "piscineiro", "jardineiro", "faxineira",
            "jornada de compra", "lide frio", "como conseguir cliente",
            "onde buscar cliente", "atrair cliente", "base de dados",
            "lista telefônica", "ligar pra desconhecido", "oferta ativa",
            "como captar", "captação de clientes", "naira barros",
            "poucos leads", "sem leads", "como aparecer", "visibilidade",
            "cold call", "lide quente", "lide morno",
        ],
    },
    {
        "id": "abordagem",
        "file": "02_abordagem.txt",
        "keywords": [
            "abordagem", "primeiro contato", "como abordar", "como falar",
            "whatsapp", "áudio", "texto", "script", "storyline",
            "e-mail", "como mandar mensagem", "como responder",
            "mensagem inicial", "como escrever", "como ligar",
            "ligação para cliente", "ligar para cliente",
            "multicanal", "sequência de contato", "como entrar em contato",
            "como apresentar", "como chamar atenção", "mensagem que converte",
            "e-mail que funciona", "como personalizar mensagem",
        ],
    },
    {
        "id": "mentalidades",
        "file": "03_mentalidades.txt",
        "keywords": [
            "mentalidade", "tipo de cliente", "investidor", "quer comprar",
            "olhando com calma", "curioso", "informático", "quadro cerebral",
            "perfil do cliente", "5 mentalidades", "cinco mentalidades",
            "como identificar o cliente", "cliente investidor",
            "como identificar perfil", "mentalidade do cliente",
            "cliente que quer comprar", "cliente que está olhando",
            "transformar em investidor", "permuta", "terreno",
        ],
    },
    {
        "id": "esteira",
        "file": "04_esteira.txt",
        "keywords": [
            "esteira", "esteira de atendimento", "expectativa", "vai pensar",
            "vai ver outras", "vai ver outros", "acompanhar cliente",
            "cliente sumiu", "não responde", "recuperar cliente",
            "perdeu confiança", "cliente frio", "cliente esfriou",
            "data futura", "só vai comprar depois", "voltar depois",
            "cliente que não respondeu", "follow-up", "sem retorno",
            "cliente parou de responder", "quando mandar mensagem",
            "quanto tempo esperar", "manter o cliente", "próximo contato",
            "nomenclatura de contato", "como salvar contato",
            "lembrete de cliente", "google calendar", "livro ata",
        ],
    },
    {
        "id": "negociacao",
        "file": "05_negociacao.txt",
        "keywords": [
            "proposta", "negociação", "negociar", "coração de pedra",
            "sangue de barata", "cpsb", "proposta baixa", "tabela",
            "contraproposta", "proprietário não retornou", "sem retorno",
            "mudança de preço", "preço mudou", "valor mudou",
            "proposta sem resposta", "como receber proposta",
            "proposta abaixo do valor", "como negociar", "como responder proposta",
            "proprietário não aceita", "vendedor não aceita",
            "como fazer proposta", "bater proposta", "botar proposta",
            "cliente quer desconto", "abaixar o preço", "baixar o valor",
            "não barre o cliente", "esperança", "prazo da proposta",
            "verificar antes de ceder", "bobo da corte",
        ],
    },
    {
        "id": "fechamento",
        "file": "06_fechamento.txt",
        "keywords": [
            "fechar", "fechamento", "assinar", "tom de voz",
            "expressão corporal", "postura", "feeling", "apresentar imóvel",
            "mostrar imóvel", "partes ruins", "problema do imóvel",
            "metro quadrado", "como apresentar", "encantamento",
            "falar de defeito", "quando falar do problema",
            "como mostrar apartamento", "roteiro de visita",
            "o que falar no imóvel", "apresentação do imóvel",
            "feeling do corretor", "vivência genérica",
            "persiana", "rampa da garagem", "posição solar",
            "para quem é esse imóvel", "o imóvel ideal para",
            "desenvolver feeling", "desenvolver um feeling", "criar feeling",
            "montar o feeling", "me ajuda com o feeling", "fazer o feeling",
            "desenvolver o feeling", "barbada",
        ],
    },
    {
        "id": "juridico",
        "file": "07_juridico.txt",
        "keywords": [
            "escritura", "cláusula resolutiva", "contrato", "atravessador",
            "partilha", "inventário", "herdeiro", "itbi", "tabelionato",
            "registro de imóveis", "jurídico", "creci",
            "termo de apresentação", "termo de visitação", "anuente",
            "iptu do imóvel", "compra parcelada", "contrato de gaveta",
            "formal de partilha", "óbito", "separação judicial",
            "imóvel de herança", "inventário do imóvel",
            "compra direto com proprietário", "sem banco",
            "venda parcelada", "sinal", "escritura pública",
        ],
    },
    {
        "id": "imoveis",
        "file": "08_imoveis.txt",
        "keywords": [
            "construtora", "padrão caixa", "minha casa minha vida", "mcmv",
            "placa", "outdoor", "descrição de imóvel", "patrimônio de afetação",
            "como descrever imóvel", "anúncio de imóvel",
            "imóvel novo", "lançamento", "incorporadora",
            "imóvel caro", "alto padrão", "avulso", "área para incorporação",
            "terreno para construtora", "imóvel em construção",
        ],
    },
    {
        "id": "ferramentas",
        "file": "09_ferramentas.txt",
        "keywords": [
            "celular", "ferramenta", "agenda", "livro-ata", "roteiro do dia",
            "organizar o dia", "horário comercial", "meta diária",
            "planilha de metas", "quantas ligações", "quantas visitas",
            "redes sociais", "quando postar", "ritmo de postagem",
            "foto de perfil", "quando ligar", "horário para ligar",
            "sexta-feira", "ligar às 21", "ligar à noite", "ligar de noite",
            "chamada de vídeo", "mostrar na tv", "netflix com altemir",
            "editar fotos", "lightroom", "fotos dos imóveis",
            "gmail de fotos", "organizar fotos", "puxa-saco",
            "40 dias", "atualizar anúncio", "meta semanal",
            "horário de trabalho", "o que fazer no dia",
            "ladrão de tempo", "perda de tempo", "foco no trabalho",
        ],
    },
    {
        "id": "apresentacao",
        "file": "10_apresentacao.txt",
        "keywords": [
            "apresentação pessoal", "roupa", "barba", "aparência", "visual",
            "vídeo selfie", "selfie", "três perguntas", "3 perguntas",
            "corretor psicólogo", "mantra", "crença", "desanimado",
            "motivação", "ouvir o cliente", "como ouvir", "o que perguntar",
            "como se vestir", "roupa do corretor", "aparência profissional",
            "como gravar vídeo selfie", "quando usar vídeo selfie",
            "terceira pergunta", "quem decide a compra", "cônjuge",
            "se isolar", "foco total", "solidão do sucesso",
            "entorno tóxico", "limpeza do entorno",
        ],
    },
    {
        "id": "parcerias",
        "file": "11_parcerias.txt",
        "keywords": [
            "parceria", "parceiro", "autônomo", "imobiliária",
            "outra cidade", "começar do zero", "começar em nova cidade",
            "área rural", "área para incorporação", "terreno grande",
            "imobiliária ou autônomo", "qual escolher",
            "nova cidade", "balneário", "piçarras", "itapema",
            "mercado novo", "cidade nova", "vender em outro lugar",
            "aluguel de temporada", "imobiliária de terceiros",
            "expansão de carteira", "cobrir duas cidades",
            "parceiro cancelou", "parceiro desapareceu",
            "terceiros vs incorporadora",
        ],
    },
    {
        "id": "curso_acesso",
        "file": "12_curso_acesso.txt",
        "keywords": [
            "mentoria", "mma", "acesso ao curso", "plataforma", "senha",
            "login", "ibraciv", "grupo vip", "aulão", "gravação",
            "certificado", "como acessar", "não consigo acessar",
            "não recebi e-mail", "esqueci a senha", "quando começa",
            "mentoria mensal", "ao vivo", "zoom", "grupo do telegram",
            "depoimento", "vídeo de depoimento", "grupo vip alunos",
        ],
    },
    {
        "id": "etica",
        "file": "13_etica.txt",
        "keywords": [
            "ética", "comissão", "abaixar comissão", "desconto na comissão",
            "cliente do outro corretor", "plantão", "honestidade",
            "credibilidade", "reputação", "baixar comissão",
            "pedir desconto", "reduzir comissão", "negociar comissão",
            "minha comissão", "quanto cobrar", "tabela de comissão",
        ],
    },
    {
        "id": "referencias",
        "file": "14_referencias.txt",
        "keywords": [
            "livro recomendado", "livro indicado", "mercado brasileiro",
            "são paulo", "goiânia", "balneário camboriú",
            "caso real", "aluno de sucesso", "resultado do aluno",
            "exemplo prático", "ligar à noite", "ligar às 21",
            "7 motivos", "itapema", "rondonópolis",
            "eric", "ricardo klein", "lailson", "nogueira", "victor",
            "caso de sucesso", "história real", "exemplo de aluno",
            "quanto ganhou", "venda de milhão",
        ],
    },
]


def route_query(query: str) -> List[str]:
    """Returns list of relevant knowledge filenames for the given query."""
    query_lower = query.lower()
    matched = []

    for topic in TOPICS:
        if any(kw in query_lower for kw in topic["keywords"]):
            matched.append(topic["file"])

    if not matched:
        matched = ["04_esteira.txt"]

    return matched


def load_knowledge_for_query(query: str) -> str:
    """Loads and concatenates relevant knowledge files for the given query.
    Always includes the general knowledge file (knowledge.txt) and base files
    (principios_gerais) for foundational context.
    """
    topic_files = route_query(query)

    # Merge base files + topic files, deduplicated, base files first
    all_files = list(dict.fromkeys(BASE_FILES + topic_files))

    sections = []

    try:
        with open(GENERAL_KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            sections.append(f.read())
    except FileNotFoundError:
        logger.warning("Arquivo de conhecimento geral não encontrado: %s", GENERAL_KNOWLEDGE_FILE)

    for filename in all_files:
        filepath = os.path.join(KNOWLEDGE_DIR, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                sections.append(f.read())
        except FileNotFoundError:
            logger.warning("Arquivo de conhecimento não encontrado: %s", filepath)

    logger.debug("Router: query=%r → arquivos=%s", query[:60], all_files)
    return "\n\n".join(sections)
