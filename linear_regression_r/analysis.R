library(MASS);
library(nortest);
library(lattice);
library(moments);

B <- Boston;

panel.hist.splom<-function(x, ...) 
{ 
	yrng <- current.panel.limits()$ylim 
	h <- hist(x, plot = FALSE) 
	breaks <- h$breaks; nB <- length(breaks) 
	y <- h$counts; y <- yrng[1] + 0.95 * diff(yrng) * y / max(y) 
	panel.rect(breaks[-nB], yrng[1], breaks[-1], y,   
			   col="cyan", ...) 
} 
panel.hist <- function(x, ...)
{
	usr <- par("usr"); on.exit(par(usr))
	par(usr = c(usr[1:2], 0, 1.5) )
	h <- hist(x, plot = FALSE)
	breaks <- h$breaks; nB <- length(breaks)
	y <- h$counts; y <- y/max(y)
	rect(breaks[-nB], 0, breaks[-1], y, col = "cyan", ...)
}
panel.cor <- function(x, y, digits = 2, prefix = "", cex.cor, ...)
{
	usr <- par("usr"); on.exit(par(usr))
	par(usr = c(0, 1, 0, 1))
	r <- abs(cor(x, y))
	txt <- format(c(r, 0.123456789), digits = digits)[1]
	txt <- paste0(prefix, txt)
	if(missing(cex.cor)) cex.cor <- 0.8/strwidth(txt)
	text(0.5, 0.5, txt, cex = cex.cor * r)
}

interest1 = c('crim', 'zn', 'indus', 'nox', 'rm', 'age', 'dis', 'rad', 'lstat', 'medv')

B$logCrim <- log(B$crim);
B$logNox <- log(B$nox);
B$logRm <- log(B$rm);
B$logMedv <- log(B$medv);
B$logLstat <- log(B$lstat);
B$logDis <- log(B$dis)

interest2 <- c('logCrim', 'zn', 'indus', 'logNox', 'logRm', 'age', 'logDis', 'rad', 'logLstat', 'logMedv')

B$group <- (B$indus < (-2.5 * B$logCrim + 15)) & (B$rad < 20)

interest3 <- c('logCrim', 'logNox', 'logRm', 'logDis', 'logLstat', 'logMedv')
interest3_pred <- c('logCrim', 'logNox', 'logRm', 'logDis', 'logLstat')


BG <- B[B$group,];

fitAll <-lm(BG$logMedv ~ BG$logCrim+BG$logNox+BG$logRm+BG$logDis+BG$logLstat);
summary(fitAll);

fitNoI <-lm(BG$logMedv ~ BG$logCrim+BG$logNox+BG$logRm+BG$logDis+BG$logLstat+0)
summary(fitNoI);

S <- cov(BG[,interest3_pred]);
M <- colMeans(BG[,interest3_pred]);

BG$mahalanobis <- mahalanobis(BG[,interest3_pred], M, S);

