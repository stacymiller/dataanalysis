library(foreign)
library(MASS)
library(candisc)
library(car)
library(psych)
library(nortest)
library(stats)
# library(qualityTools)
# library(ppcor)
# library(mixlm)
# library(QuantPsyc)
library(klaR)
# library(biotools)
df <- read.spss("wuschiz.sav",to.data.frame=TRUE)
df$Schizo==1
df <- subset(df, Schizo!=1)
#df <- read.csv("C://?????/5_????/Australian/australian.dat.txt",dec=".",sep=" ")

# boxM(df[,-c(1,2)],df$Schizo)
man <- aov(Schizo~.,df[,-1])
summary(man)

boxplot(df$Pa~df$Schizo)
shapiro.test(df$Pa[df$Schizo==0])
var.test(df$Pa[df$Schizo==0],df$Pa[df$Schizo==1])
t.test(df$Pa[df$Schizo==0],df$Pa[df$Schizo==1])

l <- lda(Schizo~.,df[,-1])
can <- candisc(lm(cbind(L,F)),df[,-1])
l
plot(l)
partimat(Schizo~.,df[,-1],method="lda") 
pre <- predict(l)
ldahist(pre$x[,1],g=df$Schizo)
ldahist(pre$x[,2],g=df$Schizo)
plot(pre$x[,1],pre$x[,2], col=df$Schizo)
text(pre$x[,1],pre$x[,2],df$Schizo,cex=0.7,pos=4,col="red") 
gree1 <- greedy.wilks(Schizo~.,df[,-1],niveau = 0.05)
gree1


#????????? ?? ?????????????? ? ????????:
df.test <- df[seq(1,nrow(df),20),]

df.train <-df[-seq(1,nrow(df),20),]
df<- na.omit(df)
l <- qda(df[,-c(1,2)],df[,2], CV = TRUE, prior=c(0.5,0.5))
l
table(l$class,df[,2])
pred <- predict(l,df[,-c(1,2)])$class

table(pred, df[,2])
man <- manova(as.matrix(df[,-c(1,2)])~pred)
summary(man, test="Wilks")

# names<-read.csv("C://?????/RR/4/Ozone2/eighthr.names.txt",header =FALSE ,
#                 na.strings = "?",skip=3)
# names <- as.character(names$V1)
# names <- gsub(names, pattern = ':     continuous.', replacement = '')
# names[72] <- 'Precp'
# names <- c('Date', names, 'Day')
# 
# df <- read.csv("C://?????/RR/4/Ozone2/eighthr.data.txt",header = FALSE,
#                na.strings = "?")
# df <- as.data.frame(df, ncoll = 74)
# names(df) <- names
# 
# df.ex.NA <- na.omit(df)
# df.ex.NA$Day <- as.factor(df.ex.NA$Day)
# l1 <- lda(Day~.,df.ex.NA[,-1])
# l1
# pre <- predict(l1)
# ldahist(pre$x[,1],g=df.ex.NA$Day)
# ldahist(pre$x[,2],g=df.ex.NA$Day)
# plot(pre$x[,1],pre$x[,2])
# plot(l1)
# partimat(Day~.,data=df.ex.NA[1:100,-c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)],method="lda") 
