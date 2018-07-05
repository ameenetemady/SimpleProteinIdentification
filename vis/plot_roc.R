library(ggplot2)
library(pracma)

myTheme <- theme(panel.grid.major = element_blank(), 
                 panel.grid.minor = element_blank(),
                 panel.background = element_blank(),
                 legend.box.background = element_blank(),
                 #legend.position =  c(0.6,0.1),
                 legend.key = element_blank(),
                 aspect.ratio=1,
                 axis.line = element_line(colour = "black"),
                 panel.border = element_rect(fill=NA, size=1),
                 text = element_text(size=16, family="Helvetica"))

get_auc <- function(x, y){
  auc <- trapz(x, y)
  return(round(auc, digits=2))
}

# ROC curves
load_roc_data <- function(df_settings){
  data_filepath <- file.path("/Users/ameen/",df_settings$dir, "pred.csv.roc")
  df_data <- read.table(data_filepath, sep=" ")
  colnames(df_data) <- c("FPR", "TPR")
  auc <- get_auc(df_data$FPR, df_data$TPR)
  df_data$method <- sprintf("%s(%.2f)", df_settings$method,auc)
  
  return (df_data)
}

load_roc_data_all_methods <- function(df_settings){
  df_all <- data.frame()
  for(method_name in unique(df_settings$method)){
    df_curr <- load_roc_data(df_settings[df_settings$method == method_name,])
    df_all <- rbind(df_all, df_curr)
  }
  return(df_all)
}

plot_roc <- function(df_settings){
  df <- load_roc_data_all_methods(df_settings)
  gPlot <- ggplot(df, aes(x=FPR, y=TPR, colour=method))+
              geom_line()+
              myTheme
  
  fig_filename <- paste("fig/roc_", unique(df_settings$dataset), ".pdf", sep = "")
  ggsave(fig_filename, gPlot)
}

df_settings <- read.table("settings.csv", sep = ",", header = TRUE)

for(dataset_name in unique(df_settings$dataset)){
  print(paste("dataset_name:", dataset_name))
  plot_roc(df_settings[df_settings$dataset==dataset_name,])
}