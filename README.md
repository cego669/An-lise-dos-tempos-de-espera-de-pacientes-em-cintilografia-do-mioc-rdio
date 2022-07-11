# Análise dos tempos de espera de pacientes em cintilografia do miocárdio

*Em medicina nuclear, os exames seguem uma logística bastante específica. Primeiro o paciente é encaminhado para a injeção do radiofármaco e, em seguida, após um intervalo de tempo determinado, são conduzidos para a aquisição das imagens (seja de PET ou de SPECT). No caso deste projeto, a análise é referente aos tempos de espera em cintilografia do miocárdio (SPECT), que é um exame constituído de duas etapas principais de imageamento: a etapa de estresse e a de repouso. As duas etapas são necessárias para estimar a perfusão do miocárdio nas condições de repouso e esforço físico, respectivamente.*

**Dados:** os dados foram anonimizados e são referentes aos horários de realização de cada etapa em cintilografia do miocárdio por cada paciente. Há dados faltantes. Neste projeto, é proposto um método de preenchimento dos dados.

**Scripts:** *preenchimento_dados_faltantes.ipynb* se refere à lógica usada para preenchimento dos dados faltantes; *video_de_fluxo_de_pacientes.ipynb* se refere ao script usado para gerar os vídeos de "fluxo" dos pacientes em cada dia de exame; *webapp.py* se refere ao código escrito para gerar o aplicativo web.

**Objetivos:** buscou-se evidenciar os dias de maior atraso (maior tempo médio de espera dos pacientes) assim como as etapas que foram as fontes de atraso. Uma ideia legal que foi posta em prática foi a dos vídeos de fluxo dos pacientes ao longo das etapas a medida que o tempo passa. Por meio deles, é possível ver, literalmente, os momentos do dia e as etapas em que há "engasgos" no atendimento aos pacientes.

Esta análise foi feita durante meu estágio na clínica Centro de Diagnóstico por Imagem (CDI).
