"""
Popula o banco com repertórios e materiais complementares verificados
para os 12 temas do Enem cadastrados.

Rodar (de dentro da pasta backend):
    ..\\venv\\Scripts\\python.exe seed_repertorios.py

Pode ser rodado mais de uma vez: o que já existe (mesmo título) é ignorado.

Formato do campo "fonte": "Texto da fonte | https://link"  — o tema.html
transforma a parte depois do "|" num link clicável.
"""
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv()

PLANALTO = "https://www.planalto.gov.br/ccivil_03"
CF = f"{PLANALTO}/constituicao/constituicao.htm"
IBGE = "https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias"

# Cada tema: lista de repertórios (titulo, descricao, como_usar, fonte)
# e lista de materiais (titulo, descricao, tipo, fonte, url).
DADOS = {
    # ───────────────────────── ENEM 2015 ─────────────────────────
    "A persistência da violência contra a mulher na sociedade brasileira": {
        "repertorios": [
            ("Lei Maria da Penha (Lei nº 11.340/2006)",
             "Criou mecanismos para coibir a violência doméstica e familiar contra a mulher, como as medidas protetivas de urgência. "
             "Leva o nome de Maria da Penha Maia Fernandes, que ficou paraplégica após ser baleada pelo marido em 1983; o caso levou "
             "a Comissão Interamericana de Direitos Humanos (OEA) a responsabilizar o Brasil por omissão em 2001.",
             "Use para mostrar que o Brasil tem lei avançada, mas que a lei sozinha não basta: o desafio é a efetivação "
             "(delegacias especializadas, casas-abrigo, fiscalização das medidas protetivas). Ótimo para a proposta de intervenção (C5).",
             f"Planalto — Lei nº 11.340/2006 | {PLANALTO}/_ato2004-2006/2006/lei/l11340.htm"),
            ("Feminicídio: de qualificadora a crime autônomo",
             "A Lei nº 13.104/2015 incluiu o feminicídio como qualificadora do homicídio. Em 2024, a Lei nº 14.994 o transformou "
             "em crime autônomo no Código Penal, com pena de 20 a 40 anos de reclusão — a maior do Código.",
             "Mostra a evolução da resposta do Estado e permite discutir por que o endurecimento penal precisa vir acompanhado de "
             "prevenção e educação para não ficar só no papel.",
             f"Planalto — Lei nº 14.994/2024 | {PLANALTO}/_ato2023-2026/2024/lei/l14994.htm"),
            ("Simone de Beauvoir — O Segundo Sexo (1949)",
             "Na frase \"Ninguém nasce mulher: torna-se mulher\", a filósofa francesa argumenta que os papéis de gênero são "
             "construídos socialmente, e não determinados pela natureza. A frase foi citada em questão do próprio Enem 2015.",
             "Repertório filosófico para a introdução ou para explicar a raiz cultural do machismo: se a desigualdade é construída, "
             "ela pode ser desconstruída pela educação (C2 e C3).",
             "Simone de Beauvoir, O Segundo Sexo (1949)"),
            ("Anuário Brasileiro de Segurança Pública (FBSP)",
             "Publicação anual do Fórum Brasileiro de Segurança Pública que reúne os registros policiais de todo o país. "
             "As edições recentes registram mais de 1.400 feminicídios por ano no Brasil, a maioria cometida por parceiros ou "
             "ex-parceiros, dentro de casa.",
             "Dado estatístico para comprovar a \"persistência\" do problema. Consulte a edição mais recente no site para citar o "
             "número exato do ano.",
             "Fórum Brasileiro de Segurança Pública | https://forumseguranca.org.br/anuario-brasileiro-seguranca-publica/"),
        ],
        "materiais": [
            ("Anuário Brasileiro de Segurança Pública",
             "Dados oficiais e atualizados sobre feminicídio e violência doméstica no Brasil.",
             "site", "Fórum Brasileiro de Segurança Pública",
             "https://forumseguranca.org.br/anuario-brasileiro-seguranca-publica/"),
            ("Texto integral da Lei Maria da Penha",
             "Lei nº 11.340/2006 no site oficial da Presidência da República.",
             "documento", "Planalto", f"{PLANALTO}/_ato2004-2006/2006/lei/l11340.htm"),
        ],
    },

    # ───────────────────────── ENEM 2026 ─────────────────────────
    "A valorização do Sistema Único de Saúde (SUS) como direito universal": {
        "repertorios": [
            ("Constituição Federal de 1988 — art. 196",
             "\"A saúde é direito de todos e dever do Estado, garantido mediante políticas sociais e econômicas que visem à redução "
             "do risco de doença e de outros agravos e ao acesso universal e igualitário às ações e serviços\".",
             "Repertório jurídico clássico para a introdução: contraste o que a Constituição garante com a realidade "
             "(filas, subfinanciamento, desigualdade regional).",
             f"Constituição Federal, art. 196 | {CF}"),
            ("Lei Orgânica da Saúde (Lei nº 8.080/1990)",
             "Regulamenta o SUS e define seus princípios: universalidade (para todos), integralidade (da prevenção ao tratamento "
             "complexo) e equidade (tratar de forma desigual os desiguais), além da participação da comunidade.",
             "Use os princípios como critério de análise: cada parágrafo pode mostrar um princípio que ainda não é plenamente cumprido.",
             f"Planalto — Lei nº 8.080/1990 | {PLANALTO}/leis/l8080.htm"),
            ("8ª Conferência Nacional de Saúde (1986)",
             "Presidida pelo sanitarista Sergio Arouca, reuniu milhares de participantes e definiu a saúde como direito do cidadão e "
             "dever do Estado. Seu relatório final serviu de base para o capítulo da saúde na Constituição de 1988 e para a criação do SUS.",
             "Repertório histórico: mostra que o SUS nasceu da mobilização da sociedade (Reforma Sanitária) — bom argumento para "
             "defender a participação social e o controle social como forma de valorização.",
             "Relatório final da 8ª CNS — Ministério da Saúde | https://bvsms.saude.gov.br/bvs/publicacoes/8_conferencia_nacional_saude_relatorio_final.pdf"),
            ("Programa Nacional de Imunizações (PNI)",
             "Criado em 1973, oferece gratuitamente pelo SUS as vacinas do calendário nacional e é referência internacional em "
             "vacinação em massa. Foi peça central na vacinação contra a Covid-19.",
             "Exemplo concreto de que o SUS funciona e alcança todo o território — útil para rebater a visão de que o sistema "
             "público é apenas \"fila\". Combina bem com a discussão sobre desinformação e queda da cobertura vacinal.",
             "Ministério da Saúde — Vacinação | https://www.gov.br/saude/pt-br/vacinacao"),
        ],
        "materiais": [
            ("Relatório final da 8ª Conferência Nacional de Saúde",
             "Documento histórico que deu origem ao SUS (PDF).",
             "documento", "Ministério da Saúde",
             "https://bvsms.saude.gov.br/bvs/publicacoes/8_conferencia_nacional_saude_relatorio_final.pdf"),
            ("Lei nº 8.080/1990 — Lei Orgânica da Saúde",
             "Texto integral da lei que regulamenta o SUS.",
             "documento", "Planalto", f"{PLANALTO}/leis/l8080.htm"),
        ],
    },

    # ───────────────────────── ENEM 2016 ─────────────────────────
    "Caminhos para combater a intolerância religiosa no Brasil": {
        "repertorios": [
            ("Constituição Federal — art. 5º, inciso VI",
             "\"É inviolável a liberdade de consciência e de crença, sendo assegurado o livre exercício dos cultos religiosos\". "
             "O Brasil é um Estado laico: não adota religião oficial e deve proteger todas.",
             "Use para afirmar que a intolerância religiosa é uma violação de direito fundamental, e não uma simples \"divergência de opinião\".",
             f"Constituição Federal, art. 5º, VI | {CF}"),
            ("Dia Nacional de Combate à Intolerância Religiosa — 21 de janeiro",
             "Instituído pela Lei nº 11.635/2007 em memória de Mãe Gilda (Gildásia dos Santos e Santos), ialorixá de Salvador que "
             "morreu em 21 de janeiro de 2000, após sofrer ataques ao seu terreiro e à sua imagem.",
             "Caso real e brasileiro que mostra que as religiões de matriz africana são as principais vítimas — conecta intolerância "
             "religiosa e racismo estrutural.",
             f"Planalto — Lei nº 11.635/2007 | {PLANALTO}/_ato2007-2010/2007/lei/l11635.htm"),
            ("Lei nº 7.716/1989 — crimes de preconceito",
             "Define como crime a discriminação por raça, cor, etnia, religião ou procedência nacional (a religião foi incluída "
             "pela Lei nº 9.459/1997). A pena para quem impede o acesso ou ofende por motivo religioso pode chegar à reclusão.",
             "Mostra que há punição prevista; o problema está na subnotificação e na impunidade — caminho para propor capacitação "
             "de policiais e divulgação de canais de denúncia como o Disque 100.",
             f"Planalto — Lei nº 7.716/1989 | {PLANALTO}/leis/l7716.htm"),
            ("John Locke — Carta sobre a Tolerância (1689)",
             "O filósofo inglês defende que o Estado não deve interferir nas crenças individuais e que a fé não pode ser imposta "
             "pela força, separando o poder civil do religioso.",
             "Repertório filosófico para fundamentar a laicidade do Estado e a convivência pacífica entre crenças diferentes.",
             "John Locke, Carta sobre a Tolerância (1689)"),
        ],
        "materiais": [
            ("Disque 100 / Ouvidoria Nacional de Direitos Humanos",
             "Canal oficial para denunciar violações de direitos humanos, incluindo intolerância religiosa.",
             "site", "Ministério dos Direitos Humanos", "https://www.gov.br/mdh/pt-br/ondh"),
            ("Lei nº 11.635/2007",
             "Lei que instituiu o Dia Nacional de Combate à Intolerância Religiosa.",
             "documento", "Planalto", f"{PLANALTO}/_ato2007-2010/2007/lei/l11635.htm"),
        ],
    },

    # ───────────────────────── ENEM 2019 ─────────────────────────
    "Democratização do acesso ao cinema no Brasil": {
        "repertorios": [
            ("Constituição Federal — art. 215",
             "\"O Estado garantirá a todos o pleno exercício dos direitos culturais e acesso às fontes da cultura nacional\".",
             "Mostra que o acesso à cultura — e ao cinema — é um direito, e não um luxo. Bom para a introdução.",
             f"Constituição Federal, art. 215 | {CF}"),
            ("Walter Benjamin — A obra de arte na era de sua reprodutibilidade técnica (1936)",
             "O filósofo alemão argumenta que o cinema, por ser reproduzível, tem potencial de levar a arte às massas, "
             "rompendo com a ideia de arte restrita a poucos.",
             "Contraponto crítico: o cinema nasceu com vocação democrática, mas no Brasil as salas se concentram em shoppings "
             "de grandes cidades, com ingressos caros — a promessa de Benjamin não se cumpriu.",
             "Walter Benjamin, A obra de arte na era de sua reprodutibilidade técnica (1936)"),
            ("Concentração das salas de cinema no Brasil",
             "Dados do Observatório Brasileiro do Cinema e do Audiovisual (OCA), da Ancine, mostram que as salas de cinema estão "
             "concentradas nas capitais e grandes cidades, enquanto a maior parte dos municípios brasileiros não tem nenhuma sala.",
             "Dado para comprovar a desigualdade geográfica de acesso. Consulte o painel do OCA para citar o número mais recente.",
             "Observatório Brasileiro do Cinema e do Audiovisual (Ancine) | https://www.gov.br/ancine/pt-br/oca"),
            ("Cinema Novo — \"Uma câmera na mão e uma ideia na cabeça\"",
             "Lema associado a Glauber Rocha e ao Cinema Novo (anos 1960), movimento que defendia um cinema brasileiro feito com "
             "poucos recursos e voltado à realidade do país.",
             "Repertório cultural para defender a produção audiovisual local e o cinema como forma de o brasileiro se reconhecer "
             "na tela — argumento para incentivar cineclubes e produção regional.",
             "Movimento Cinema Novo (Glauber Rocha, anos 1960)"),
        ],
        "materiais": [
            ("Observatório Brasileiro do Cinema e do Audiovisual (OCA)",
             "Dados oficiais da Ancine sobre salas, público e bilheteria no Brasil.",
             "site", "Ancine", "https://www.gov.br/ancine/pt-br/oca"),
        ],
    },

    # ───────────────────────── ENEM 2017 ─────────────────────────
    "Desafios para a formação educacional de surdos no Brasil": {
        "repertorios": [
            ("Lei da Libras (Lei nº 10.436/2002)",
             "Reconhece a Língua Brasileira de Sinais (Libras) como meio legal de comunicação e expressão das comunidades surdas. "
             "Foi regulamentada pelo Decreto nº 5.626/2005, que tornou a Libras disciplina obrigatória nos cursos de formação de professores.",
             "Mostra o avanço legal e permite questionar a prática: faltam intérpretes e professores fluentes em Libras nas escolas.",
             f"Planalto — Lei nº 10.436/2002 | {PLANALTO}/leis/2002/l10436.htm"),
            ("Educação bilíngue de surdos (Lei nº 14.191/2021)",
             "Alterou a LDB para incluir a educação bilíngue de surdos como modalidade de ensino independente, tendo a Libras "
             "como primeira língua e o português escrito como segunda.",
             "Repertório atual e preciso para a proposta de intervenção: ampliar escolas e classes bilíngues previstas na própria lei.",
             f"Planalto — Lei nº 14.191/2021 | {PLANALTO}/_ato2019-2022/2021/lei/l14191.htm"),
            ("Instituto Nacional de Educação de Surdos (INES) — 1857",
             "Fundado no Rio de Janeiro em 1857, durante o Império de D. Pedro II, com a participação do professor surdo francês "
             "Ernest Huet. É a primeira escola para surdos do Brasil e a origem histórica da Libras.",
             "Repertório histórico: mais de 160 anos depois, a educação de surdos ainda é um desafio — evidencia a lentidão das "
             "políticas públicas.",
             "INES — Ministério da Educação | https://www.gov.br/ines/pt-br"),
            ("Congresso de Milão (1880) e o oralismo",
             "Congresso internacional de educadores que decidiu pela proibição das línguas de sinais no ensino de surdos, "
             "impondo o oralismo (forçar a fala e a leitura labial). A decisão influenciou a educação de surdos por cerca de um século.",
             "Ótimo para análise crítica: mostra que a exclusão dos surdos foi construída historicamente por ouvintes que decidiram "
             "por eles — reforça a importância de respeitar a Libras como língua.",
             "Congresso Internacional de Educadores de Surdos, Milão (1880)"),
        ],
        "materiais": [
            ("Instituto Nacional de Educação de Surdos (INES)",
             "Site oficial do INES, referência nacional em educação de surdos.",
             "site", "Ministério da Educação", "https://www.gov.br/ines/pt-br"),
            ("Lei nº 14.191/2021 — educação bilíngue de surdos",
             "Texto integral da lei.",
             "documento", "Planalto", f"{PLANALTO}/_ato2019-2022/2021/lei/l14191.htm"),
        ],
    },

    # ───────────────────────── ENEM 2024 ─────────────────────────
    "Desafios para a valorização da herança africana no Brasil": {
        "repertorios": [
            ("Lei nº 10.639/2003 — ensino de história e cultura afro-brasileira",
             "Tornou obrigatório o ensino de História e Cultura Afro-Brasileira nas escolas (depois ampliada pela Lei nº 11.645/2008 "
             "para incluir a cultura indígena). Mais de 20 anos depois, sua aplicação ainda é desigual.",
             "Excelente para a proposta de intervenção (C5): formação de professores e materiais didáticos para efetivar a lei.",
             f"Planalto — Lei nº 10.639/2003 | {PLANALTO}/leis/2003/l10.639.htm"),
            ("Censo 2022: maioria da população é negra",
             "Segundo o IBGE, em 2022 45,3% dos brasileiros se declararam pardos e 10,2% pretos — juntos, 55,5% da população. "
             "Foi a primeira vez desde 1991 que os pardos se tornaram o maior grupo.",
             "Dado para mostrar a contradição: a maioria da população tem ascendência africana, mas essa herança ainda é "
             "marginalizada na escola, na mídia e nos espaços de poder.",
             f"IBGE — Censo 2022 | {IBGE}/38719-censo-2022-pela-primeira-vez-desde-1991-a-maior-parte-da-populacao-do-brasil-se-declara-parda"),
            ("Cais do Valongo — Patrimônio Mundial da UNESCO (2017)",
             "Sítio arqueológico no Rio de Janeiro onde desembarcaram centenas de milhares de africanos escravizados. É considerado "
             "o vestígio mais importante da chegada de africanos escravizados às Américas.",
             "Repertório histórico concreto: a memória da escravidão é reconhecida internacionalmente, mas ainda pouco conhecida "
             "pelos próprios brasileiros.",
             "UNESCO — Valongo Wharf Archaeological Site | https://whc.unesco.org/en/list/1548"),
            ("Feriado nacional de 20 de novembro (Lei nº 14.759/2023)",
             "O Dia Nacional de Zumbi e da Consciência Negra tornou-se feriado nacional em 2023. A data homenageia Zumbi dos "
             "Palmares, líder do maior quilombo do período colonial, morto em 20 de novembro de 1695.",
             "Mostra um avanço simbólico recente e permite discutir a diferença entre reconhecimento simbólico e valorização real.",
             f"Planalto — Lei nº 14.759/2023 | {PLANALTO}/_ato2023-2026/2023/lei/l14759.htm"),
        ],
        "materiais": [
            ("Cais do Valongo na UNESCO",
             "Página oficial do sítio na lista de Patrimônio Mundial (em inglês).",
             "site", "UNESCO", "https://whc.unesco.org/en/list/1548"),
            ("Censo 2022: população por cor ou raça",
             "Notícia oficial do IBGE com os dados de cor ou raça do Censo 2022.",
             "reportagem", "IBGE",
             f"{IBGE}/38719-censo-2022-pela-primeira-vez-desde-1991-a-maior-parte-da-populacao-do-brasil-se-declara-parda"),
        ],
    },

    # ───────────────────────── ENEM 2022 ─────────────────────────
    "Desafios para a valorização de comunidades e povos tradicionais no Brasil": {
        "repertorios": [
            ("Decreto nº 6.040/2007 — quem são os povos tradicionais",
             "Institui a Política Nacional de Desenvolvimento Sustentável dos Povos e Comunidades Tradicionais e os define como "
             "grupos culturalmente diferenciados, que usam territórios e recursos naturais para sua reprodução cultural, social, "
             "religiosa e econômica (ex.: indígenas, quilombolas, ribeirinhos, quebradeiras de coco, caiçaras).",
             "Use na introdução para delimitar o tema — mostra domínio do conceito (C2).",
             f"Planalto — Decreto nº 6.040/2007 | {PLANALTO}/_ato2007-2010/2007/decreto/d6040.htm"),
            ("Censo 2022: indígenas e quilombolas",
             "O IBGE contou 1.693.535 indígenas em 2022 (0,83% da população) e, pela primeira vez na história, recenseou os "
             "quilombolas: cerca de 1,3 milhão de pessoas em 1.696 municípios.",
             "Dado que mostra que esses povos foram estatisticamente invisíveis até muito recentemente — o primeiro passo para "
             "políticas públicas é contá-los.",
             f"IBGE — Censo 2022 | {IBGE}/37565-brasil-tem-1-7-milhao-de-indigenas-e-mais-da-metade-deles-vive-na-amazonia-legal"),
            ("Convenção 169 da OIT — consulta prévia",
             "Tratado internacional ratificado pelo Brasil que garante aos povos indígenas e tribais o direito à consulta prévia, "
             "livre e informada sobre medidas e empreendimentos que os afetem. Hoje está consolidada no Decreto nº 10.088/2019.",
             "Argumento forte para criticar obras e projetos feitos sem ouvir as comunidades (garimpo, hidrelétricas, rodovias).",
             f"Planalto — Decreto nº 10.088/2019 | {PLANALTO}/_ato2019-2022/2019/decreto/d10088.htm"),
            ("Ailton Krenak — Ideias para adiar o fim do mundo (2019)",
             "O pensador indígena critica a ideia de \"humanidade\" separada da natureza e mostra que os povos tradicionais "
             "preservam modos de vida que mantêm a floresta em pé.",
             "Repertório que inverte a lógica: os povos tradicionais não são \"atrasados\", mas guardiões de saberes essenciais "
             "diante da crise climática.",
             "Ailton Krenak, Ideias para adiar o fim do mundo (Companhia das Letras, 2019)"),
        ],
        "materiais": [
            ("Censo 2022: Brasil tem 1,7 milhão de indígenas",
             "Notícia oficial do IBGE.",
             "reportagem", "IBGE",
             f"{IBGE}/37565-brasil-tem-1-7-milhao-de-indigenas-e-mais-da-metade-deles-vive-na-amazonia-legal"),
            ("Censo 2022: Brasil tem 1,3 milhão de quilombolas",
             "Notícia oficial do IBGE sobre o primeiro recenseamento quilombola.",
             "reportagem", "IBGE", f"{IBGE}/37464-brasil-tem-1-3-milhao-de-quilombolas-em-1-696-municipios"),
        ],
    },

    # ───────────────────────── ENEM 2023 ─────────────────────────
    "Desafios para o enfrentamento da invisibilidade do trabalho de cuidado realizado pela mulher no Brasil": {
        "repertorios": [
            ("IBGE: mulheres dedicam quase o dobro de horas ao cuidado",
             "Segundo a PNAD Contínua do IBGE, em 2022 as mulheres dedicaram em média 21,3 horas semanais aos afazeres domésticos "
             "e/ou ao cuidado de pessoas, contra 11,7 horas dos homens — uma diferença de 9,6 horas por semana.",
             "Principal dado estatístico do tema. Use para comprovar a desigualdade e a \"dupla jornada\" feminina.",
             f"IBGE — PNAD Contínua 2022 | {IBGE}/37621-em-2022-mulheres-dedicaram-9-6-horas-por-semana-a-mais-do-que-os-homens-aos-afazeres-domesticos-ou-ao-cuidado-de-pessoas"),
            ("Oxfam — relatório \"Tempo de Cuidar\" (2020)",
             "A Oxfam estimou que o trabalho de cuidado não remunerado feito por mulheres e meninas no mundo valeria quase "
             "11 trilhões de dólares por ano se fosse pago.",
             "Mostra que o cuidado é trabalho com valor econômico real — por isso sua invisibilidade é um problema econômico, não só moral.",
             "Oxfam International — Time to Care | https://www.oxfam.org/en/research/time-care"),
            ("Política Nacional de Cuidados (Lei nº 15.069/2024)",
             "Lei que institui a Política Nacional de Cuidados, reconhecendo o cuidado como direito e prevendo a "
             "corresponsabilidade entre Estado, famílias, setor privado e sociedade, além da divisão entre homens e mulheres.",
             "Repertório atual para a proposta de intervenção: mostre que a lei existe e proponha como implementá-la "
             "(creches, centros-dia para idosos, licença-paternidade).",
             f"Planalto — Lei nº 15.069/2024 | {PLANALTO}/_ato2023-2026/2024/lei/l15069.htm"),
            ("Silvia Federici — \"O que eles chamam de amor, nós chamamos de trabalho não pago\"",
             "A filósofa ítalo-americana, no texto \"Salários contra o trabalho doméstico\" (1975), argumenta que o trabalho doméstico "
             "foi naturalizado como \"dom feminino\" para não ser reconhecido nem remunerado.",
             "Repertório filosófico que explica a raiz da invisibilidade: a naturalização do cuidado como amor/instinto.",
             "Silvia Federici, Salários contra o trabalho doméstico (1975)"),
        ],
        "materiais": [
            ("IBGE: mulheres dedicam 9,6 horas a mais por semana ao cuidado",
             "Notícia oficial do IBGE com os dados da PNAD Contínua 2022.",
             "reportagem", "IBGE",
             f"{IBGE}/37621-em-2022-mulheres-dedicaram-9-6-horas-por-semana-a-mais-do-que-os-homens-aos-afazeres-domesticos-ou-ao-cuidado-de-pessoas"),
            ("Oxfam — Time to Care",
             "Relatório internacional sobre o trabalho de cuidado (em inglês).",
             "documento", "Oxfam International", "https://www.oxfam.org/en/research/time-care"),
        ],
    },

    # ───────────────────────── ENEM 2021 ─────────────────────────
    "Invisibilidade e registro civil: garantia de acesso à cidadania no Brasil": {
        "repertorios": [
            ("Declaração Universal dos Direitos Humanos — art. 6º",
             "\"Todo ser humano tem o direito de ser, em todos os lugares, reconhecido como pessoa perante a lei.\" "
             "Sem certidão de nascimento, a pessoa não existe oficialmente para o Estado.",
             "Repertório para a introdução: o registro civil é a porta de entrada para todos os outros direitos.",
             "DUDH (ONU, 1948) — UNICEF | https://www.unicef.org/brazil/declaracao-universal-dos-direitos-humanos"),
            ("Hannah Arendt — o \"direito a ter direitos\"",
             "Em \"Origens do Totalitarismo\" (1951), a filósofa mostra que pessoas sem vínculo reconhecido com um Estado (como os "
             "apátridas) perdem na prática o acesso a todos os direitos — o primeiro direito é o de pertencer.",
             "Repertório filosófico forte: quem não tem registro civil vive situação semelhante, invisível para as políticas públicas.",
             "Hannah Arendt, Origens do Totalitarismo (1951)"),
            ("Gratuidade do registro de nascimento (Lei nº 9.534/1997)",
             "A Constituição (art. 5º, LXXVI) garantia a gratuidade do registro aos reconhecidamente pobres; a Lei nº 9.534/1997 "
             "estendeu a gratuidade da certidão de nascimento e de óbito a todos os brasileiros.",
             "Mostra que o custo não é mais a barreira: o problema hoje está na distância dos cartórios, na falta de informação "
             "e em populações vulneráveis (ribeirinhos, indígenas, pessoas em situação de rua).",
             f"Planalto — Lei nº 9.534/1997 | {PLANALTO}/leis/l9534.htm"),
            ("Graciliano Ramos — Vidas Secas (1938)",
             "Fabiano, retirante nordestino, é humilhado e preso sem conseguir se defender, sentindo-se \"um bicho\". "
             "A obra retrata pessoas à margem do Estado e da cidadania.",
             "Repertório literário para ilustrar a invisibilidade social de quem está fora do alcance das instituições.",
             "Graciliano Ramos, Vidas Secas (1938)"),
        ],
        "materiais": [
            ("Declaração Universal dos Direitos Humanos",
             "Texto completo da DUDH em português.",
             "documento", "UNICEF Brasil", "https://www.unicef.org/brazil/declaracao-universal-dos-direitos-humanos"),
        ],
    },

    # ───────────────────────── ENEM 2018 ─────────────────────────
    "Manipulação do comportamento do usuário pelo controle de dados na internet": {
        "repertorios": [
            ("Escândalo Cambridge Analytica (2018)",
             "Reportagens do The Guardian e do The New York Times revelaram que a consultoria Cambridge Analytica obteve dados de "
             "até 87 milhões de usuários do Facebook sem consentimento, usados para direcionar propaganda política.",
             "Exemplo real e de impacto mundial de manipulação de comportamento por dados — ótimo para o desenvolvimento.",
             "The Guardian — The Cambridge Analytica Files | https://www.theguardian.com/news/series/cambridge-analytica-files"),
            ("Lei Geral de Proteção de Dados (Lei nº 13.709/2018)",
             "A LGPD regula o tratamento de dados pessoais no Brasil, exige consentimento e finalidade clara para a coleta e criou "
             "a Autoridade Nacional de Proteção de Dados (ANPD) para fiscalizar.",
             "Mostra a resposta do Estado; permite criticar que a lei é pouco conhecida pelos usuários — caminho para propor "
             "educação digital.",
             f"Planalto — Lei nº 13.709/2018 | {PLANALTO}/_ato2015-2018/2018/lei/l13709.htm"),
            ("Shoshana Zuboff — \"Capitalismo de vigilância\" (2019)",
             "A pesquisadora de Harvard descreve um modelo de negócio em que as big techs coletam a experiência humana como "
             "matéria-prima para prever e modificar comportamentos, vendendo essas previsões.",
             "Conceito sofisticado para explicar a causa do problema: o usuário não é o cliente, é o produto.",
             "Shoshana Zuboff, A era do capitalismo de vigilância (2019)"),
            ("Documentário \"O Dilema das Redes\" (2020)",
             "Documentário da Netflix com ex-funcionários de Google, Facebook e outras empresas explicando como os algoritmos são "
             "projetados para prender a atenção e influenciar escolhas.",
             "Repertório cultural acessível — mostra que os próprios criadores das plataformas reconhecem a manipulação.",
             "The Social Dilemma (O Dilema das Redes), dir. Jeff Orlowski, Netflix (2020)"),
        ],
        "materiais": [
            ("The Cambridge Analytica Files",
             "Série de reportagens do The Guardian que revelou o escândalo (em inglês).",
             "reportagem", "The Guardian", "https://www.theguardian.com/news/series/cambridge-analytica-files"),
            ("Lei Geral de Proteção de Dados (LGPD)",
             "Texto integral da Lei nº 13.709/2018.",
             "documento", "Planalto", f"{PLANALTO}/_ato2015-2018/2018/lei/l13709.htm"),
        ],
    },

    # ───────────────────────── ENEM 2020 ─────────────────────────
    "O estigma associado às doenças mentais na sociedade brasileira": {
        "repertorios": [
            ("Holocausto Brasileiro — Daniela Arbex (2013)",
             "Livro-reportagem sobre o Hospital Colônia de Barbacena (MG), onde cerca de 60 mil pessoas morreram ao longo do "
             "século XX. Muitas internadas nem tinham doença mental: eram pobres, alcoolistas, mães solteiras, homossexuais.",
             "Repertório histórico impactante: mostra como o estigma serviu para excluir os \"indesejados\" da sociedade.",
             "Daniela Arbex, Holocausto Brasileiro (Geração Editorial, 2013)"),
            ("Reforma Psiquiátrica (Lei nº 10.216/2001)",
             "Conhecida como Lei Paulo Delgado, protege os direitos das pessoas com transtornos mentais e redireciona o "
             "tratamento dos manicômios para serviços comunitários, como os CAPS (Centros de Atenção Psicossocial).",
             "Mostra o avanço legal e permite discutir que a rede de CAPS ainda é insuficiente — ótimo para a proposta de intervenção.",
             f"Planalto — Lei nº 10.216/2001 | {PLANALTO}/leis/leis_2001/l10216.htm"),
            ("OMS: Brasil lidera em transtornos de ansiedade",
             "No relatório \"Depression and Other Common Mental Disorders: Global Health Estimates\" (2017), a Organização Mundial "
             "da Saúde apontou o Brasil como o país com a maior prevalência de transtornos de ansiedade do mundo (9,3% da população).",
             "Dado que mostra que a doença mental é comum — o que torna o estigma ainda mais injustificável.",
             "Organização Mundial da Saúde (2017) | https://www.who.int/publications/i/item/depression-global-health-estimates"),
            ("Erving Goffman — Estigma (1963)",
             "O sociólogo define estigma como um atributo que \"desacredita\" a pessoa e a reduz a uma única característica, "
             "levando à exclusão social.",
             "Conceito central do tema: use para explicar por que muitas pessoas evitam buscar tratamento por medo do rótulo de \"louco\".",
             "Erving Goffman, Estigma: notas sobre a manipulação da identidade deteriorada (1963)"),
        ],
        "materiais": [
            ("Depression and Other Common Mental Disorders (OMS)",
             "Relatório da OMS com dados globais sobre depressão e ansiedade (em inglês).",
             "documento", "Organização Mundial da Saúde",
             "https://www.who.int/publications/i/item/depression-global-health-estimates"),
            ("Lei nº 10.216/2001 — Reforma Psiquiátrica",
             "Texto integral da lei.",
             "documento", "Planalto", f"{PLANALTO}/leis/leis_2001/l10216.htm"),
        ],
    },

    # ───────────────────────── ENEM 2025 ─────────────────────────
    "Perspectivas acerca do envelhecimento na sociedade brasileira": {
        "repertorios": [
            ("Censo 2022: Brasil está envelhecendo rápido",
             "Segundo o IBGE, a população com 60 anos ou mais passou de 32 milhões em 2022. O índice de envelhecimento chegou a 80 "
             "idosos para cada 100 crianças de 0 a 14 anos; no Rio Grande do Sul e no Rio de Janeiro já há mais idosos que crianças.",
             "Dado central do tema: mostra que o envelhecimento é uma realidade presente, que exige adaptação de saúde, "
             "previdência, mobilidade e mercado de trabalho.",
             f"IBGE — Censo 2022 | {IBGE}/38186-censo-2022-numero-de-pessoas-com-65-anos-ou-mais-de-idade-cresceu-57-4-em-12-anos"),
            ("Estatuto da Pessoa Idosa (Lei nº 10.741/2003)",
             "Garante direitos às pessoas com 60 anos ou mais, como prioridade no atendimento, proteção contra violência e "
             "abandono e acesso à saúde. Em 2022, passou a se chamar Estatuto da Pessoa Idosa.",
             "Use para contrastar a lei com a realidade (etarismo, abandono, violência financeira contra idosos).",
             f"Planalto — Lei nº 10.741/2003 | {PLANALTO}/leis/2003/l10.741.htm"),
            ("Constituição Federal — art. 230",
             "\"A família, a sociedade e o Estado têm o dever de amparar as pessoas idosas, assegurando sua participação na "
             "comunidade, defendendo sua dignidade e bem-estar e garantindo-lhes o direito à vida.\"",
             "Bom para mostrar que a responsabilidade é compartilhada — ajuda a definir os agentes da proposta de intervenção (C5).",
             f"Constituição Federal, art. 230 | {CF}"),
            ("Década do Envelhecimento Saudável (ONU/OMS, 2021–2030)",
             "Iniciativa da ONU, coordenada pela OMS, para melhorar a vida das pessoas idosas, combater o etarismo e criar "
             "cidades e comunidades amigas da pessoa idosa.",
             "Repertório internacional atual — mostra que o Brasil pode se inspirar em compromissos globais.",
             "OPAS/OMS — Década do Envelhecimento Saudável | https://www.paho.org/pt/decada-do-envelhecimento-saudavel-nas-americas-2021-2030"),
            ("Simone de Beauvoir — A Velhice (1970)",
             "A filósofa denuncia que a sociedade trata os idosos como \"inúteis\" quando deixam de produzir, revelando uma "
             "visão que mede o valor humano pela produtividade.",
             "Repertório filosófico para criticar o etarismo e a lógica produtivista.",
             "Simone de Beauvoir, A Velhice (1970)"),
        ],
        "materiais": [
            ("Censo 2022: população idosa no Brasil",
             "Notícia oficial do IBGE sobre o envelhecimento da população.",
             "reportagem", "IBGE",
             f"{IBGE}/38186-censo-2022-numero-de-pessoas-com-65-anos-ou-mais-de-idade-cresceu-57-4-em-12-anos"),
            ("Década do Envelhecimento Saudável nas Américas",
             "Página oficial da OPAS/OMS sobre a iniciativa.",
             "site", "OPAS/OMS", "https://www.paho.org/pt/decada-do-envelhecimento-saudavel-nas-americas-2021-2030"),
        ],
    },
}


def main():
    con = mysql.connector.connect(
        host=os.getenv("DB_HOST"), user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"), database=os.getenv("DB_NAME"),
    )
    cur = con.cursor()

    cur.execute("SELECT id_usuario FROM USUARIO WHERE perfil = 'administrador' ORDER BY id_usuario LIMIT 1")
    linha = cur.fetchone()
    if not linha:
        raise SystemExit("Nenhum administrador cadastrado. Rode criar_admin.py primeiro.")
    id_admin = linha[0]

    novos_r = novos_m = 0
    for titulo_tema, dados in DADOS.items():
        cur.execute("SELECT id_tema FROM TEMA WHERE titulo = %s", (titulo_tema,))
        t = cur.fetchone()
        if not t:
            print(f"[aviso] tema não encontrado: {titulo_tema}")
            continue
        id_tema = t[0]

        for titulo, descricao, como_usar, fonte in dados["repertorios"]:
            assert len(titulo) <= 200 and len(fonte) <= 255, titulo
            cur.execute("SELECT id_repertorio FROM REPERTORIO WHERE titulo = %s", (titulo,))
            r = cur.fetchone()
            if r:
                id_rep = r[0]
            else:
                cur.execute(
                    "INSERT INTO REPERTORIO (titulo, descricao, como_usar, fonte, id_usuario_criador) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (titulo, descricao, como_usar, fonte, id_admin),
                )
                id_rep = cur.lastrowid
                novos_r += 1
            cur.execute("INSERT IGNORE INTO TEMA_REPERTORIO (id_tema, id_repertorio) VALUES (%s, %s)",
                        (id_tema, id_rep))

        for titulo, descricao, tipo, fonte, url in dados["materiais"]:
            assert len(titulo) <= 200 and len(fonte) <= 150 and len(url) <= 500, titulo
            cur.execute("SELECT id_material FROM MATERIAL_COMPLEMENTAR WHERE titulo = %s", (titulo,))
            m = cur.fetchone()
            if m:
                id_mat = m[0]
            else:
                cur.execute(
                    "INSERT INTO MATERIAL_COMPLEMENTAR (titulo, descricao, tipo, fonte, url, id_usuario_criador) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (titulo, descricao, tipo, fonte, url, id_admin),
                )
                id_mat = cur.lastrowid
                novos_m += 1
            cur.execute("INSERT IGNORE INTO TEMA_MATERIAL (id_tema, id_material) VALUES (%s, %s)",
                        (id_tema, id_mat))

    con.commit()
    cur.close()
    con.close()
    print(f"Pronto: {novos_r} repertórios e {novos_m} materiais novos inseridos.")


if __name__ == "__main__":
    main()
