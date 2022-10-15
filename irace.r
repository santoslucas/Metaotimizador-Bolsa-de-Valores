library(stats)
library(doParallel)
library(irace)
library(reticulate)

setwd("/Users/lucas/OneDrive/Documentos/metaOtimizador/Semana_C_T")

#py_install("numpy")
#py_install("pandas")
#py_install("yfinance")
#py_install("ta-lib")
#py_install("matplotlib.pyplot")
#py_install("matplotlib.dates")

np <- import("numpy")
pd <- import("pandas")
yf <- import("yfinance")
ta <- import("talib")
plt <- import("matplotlib.pyplot")
mdates <- import("matplotlib.dates")

source_python('funcoes.py')

#configuracao para a sintonia de parametros
parametros.tabela <- '
x0 "" c (open,close,low,high)
x1 "" i (2, 8)
x2 "" i (2, 8)
x3 "" r (0.01, 0.15)
x4 "" r (0.01, 0.15)
'
obj_funs <- c(1L, 2L, 3L)

#le tabela para o irace
parameters <- readParameters(text = parametros.tabela)

#funcao para avaliar cada candidato de configuracao em uma instancia
target.runner <- function(experiment, scenario) {
  instance <- experiment$instance
  # print(instances)
  configuration <- experiment$configuration

  #executa o ga
  obj <- heuristica1treino( 
     as.array(configuration[['x0']]), 
     as.integer(configuration[['x1']]),
     as.integer(configuration[['x2']]),
     as.double(configuration[['x3']]),
     as.double(configuration[['x4']]),
     ticker = 'aapl'
     )
  
  #print(obj)
  return (list(cost = obj))
}

#configuracao do cenario
scenario <- list(targetRunner = target.runner,
                 instances = obj_funs,
                 maxExperiments = 5000,
                 logFile = 'irace-log.txt')

#verifica se o cenario e valido
checkIraceScenario(scenario = scenario, parameters = parameters)

#executa o irace
tuned.confs <- irace(scenario = scenario, parameters = parameters)

#apresentar os melhores conjuntos de parametros para as tres funcoes objetivo
configurations.print(tuned.confs)

#testa as configuracoes
test <- function(configuration)
{
  res <- lapply(matrix(rep(obj_funs,each=1), nrow=length(obj_funs)*5),
                function(x) target.runner(
                  experiment = list(instance = x, configuration = configuration),
                  scenario = scenario)
                )
  return (sapply(res, getElement, name = "cost"))
}

default <- test(data.frame(x0='close', x1=3, x2=6, x3=0.1, x4=0.1, ticker='aapl'))

tuned1 <- test (removeConfigurationsMetaData(tuned.confs[1,]))

tuned2 <- test (removeConfigurationsMetaData(tuned.confs[2,]))

boxplot(list(default=default, tuned1=tuned1, tuned2=tuned2))

