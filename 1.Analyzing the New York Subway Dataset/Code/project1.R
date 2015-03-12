# Package Loading
library(data.table)
library(ggmap)
library(pander)
library(fBasics)
library(quantmod)
library(randomForest)
library(ggplot2)


# Data Loading
raw.data <- fread(input="turnstile_weather_v2.csv", header=TRUE)

# Statistical Test
enter.rain <- raw.data[rain==1,ENTRIESn_hourly]
enter.norain <- raw.data[rain==0,ENTRIESn_hourly]
par(mfrow=c(1,2))
qqnormPlot(enter.rain)
qqnormPlot(enter.norain)
par(mfrow=c(1,1))
mat <- matrix(0,2,2); dimnames(mat) <- list(c("Mean","Median"),c("Rain","NoRain"))
mat['Mean','Rain'] <- mean(enter.rain)
mat['Mean','NoRain'] <- mean(enter.norain)
mat['Median','Rain'] <- median(enter.rain)
mat['Median','NoRain'] <- median(enter.norain)
pander(mat)
wilcox.test(enter.rain, enter.norain, alternative="two.sided")

# Linear Regression - 1
data1 <- raw.data[,.(ENTRIESn_hourly,weekday,fog,rain,as.factor(hour),as.factor(station),
                    precipi,pressurei,tempi,wspdi,meanprecipi,meanpressurei,meantempi,meanwspdi)]
# OLS - 1
model.ols1 <- lm(ENTRIESn_hourly~., data=data1)
summary(model.ols1)

# Linear Regression - 2
data2 <- data.table()
station <- unique(raw.data[,station])
for(i in 1:length(station)){
  data.temp <- raw.data[station==station[i],][,.(ENTRIESn_hourly,weekday,fog,rain,as.factor(hour),as.factor(station),
                                                 precipi,pressurei,tempi,wspdi,meanprecipi,meanpressurei,meantempi,meanwspdi)]
  data.temp2 <- cbind(data.temp, Lag(data.temp[,ENTRIESn_hourly], k=1))
  data.temp3 <- na.omit(data.temp2)
  data2 <- rbind(data2, data.temp3)
}
# OLS - 2
model.ols2 <- lm(ENTRIESn_hourly~., data=data2)
summary(model.ols2)

# Linear Regression - 3
data3 <- data.table()
station <- unique(raw.data[,station])
for(i in 1:length(station)){
  data.temp <- raw.data[station==station[i],][,.(ENTRIESn_hourly,weekday,fog,rain,as.factor(hour),
                                                 precipi,pressurei,tempi,wspdi,meanprecipi,meanpressurei,meantempi,meanwspdi)]
  data.temp2 <- cbind(data.temp, Lag(data.temp[,ENTRIESn_hourly], k=1), Lag(data.temp[,ENTRIESn_hourly], k=2)
                      , Lag(data.temp[,ENTRIESn_hourly], k=3), Lag(data.temp[,ENTRIESn_hourly], k=4)
                      , Lag(data.temp[,ENTRIESn_hourly], k=5), Lag(data.temp[,ENTRIESn_hourly], k=6))
  data.temp3 <- na.omit(data.temp2)
  data3 <- rbind(data3, data.temp3)
}
# OLS - 3
model.ols3 <- lm(ENTRIESn_hourly~., data=data3)
summary(model.ols3)
pander(summary(model.ols3))


# Linear Regression - 4
data4 <- data.table()
station <- unique(raw.data[,station])
for(i in 1:length(station)){
  data.temp <- raw.data[station==station[i],][,.(log(1+ENTRIESn_hourly),weekday,fog,rain,hour=as.factor(hour),
                                                 precipi,pressurei,tempi,wspdi,meanprecipi,meanpressurei,meantempi,meanwspdi)]
  data.temp2 <- cbind(data.temp, Lag(data.temp[,V1], k=1), Lag(data.temp[,V1], k=2)
                      , Lag(data.temp[,V1], k=3), Lag(data.temp[,V1], k=4)
                      , Lag(data.temp[,V1], k=5), Lag(data.temp[,V1], k=6))
  data.temp3 <- na.omit(data.temp2)
  data4 <- rbind(data4, data.temp3)
}
# OLS - 4
model.ols4 <- lm(V1~., data=data4)
summary(model.ols4)
pander(summary(model.ols4))


# Beyond Linearity
data5 <- data.table()
station <- unique(raw.data[,station])
for(i in 1:length(station)){
  data.temp <- raw.data[station==station[i],][,.(log(1+ENTRIESn_hourly),day_week,fog,rain,hour,
                                                 precipi,pressurei,tempi,wspdi,meanprecipi,meanpressurei,meantempi,meanwspdi)]
  data.temp2 <- cbind(data.temp, Lag(data.temp[,V1], k=1), Lag(data.temp[,V1], k=2)
                      , Lag(data.temp[,V1], k=3), Lag(data.temp[,V1], k=4)
                      , Lag(data.temp[,V1], k=5), Lag(data.temp[,V1], k=6))
  data.temp3 <- na.omit(data.temp2)
  data5 <- rbind(data5, data.temp3)
}
set.seed(7)
model.rf <- randomForest(V1~., data=data5, ntree=5)
model.rf
plot(model.rf)
varImpPlot(model.rf)

par(mfrow=c(2,2))
partialPlot(model.rf, pred.data=data5, x.var="hour")
partialPlot(model.rf, pred.data=data5, x.var="tempi")
partialPlot(model.rf, pred.data=data5, x.var="day_week")
partialPlot(model.rf, pred.data=data5, x.var="Lag.6")
par(mfrow=c(1,1))

# Visualization
qplot(enter.rain, geom="histogram", binwidth=100)
qplot(enter.norain, geom="histogram", binwidth=100)

aggregate(raw.data[,.(day_week,rain,ENTRIESn_hourly)],by=list(raw.data[,day_week],raw.data[,rain]),FUN=mean)
mean.rain <- raw.data[rain==1,mean(ENTRIESn_hourly),by=day_week]
qplot(0:6, mean.rain[order(mean.rain[,day_week]),V1],main="Rain", geom="line", ylim=c(0,2800), xlab='mean', ylab='weekday')
mean.norain <- raw.data[rain==0,mean(ENTRIESn_hourly),by=day_week]
qplot(0:6, mean.norain[order(mean.norain[,day_week]),V1],main="NoRain", geom="line", ylim=c(0,2500), xlab='mean', ylab='weekday')


mean.rain <- raw.data[rain==1,mean(ENTRIESn_hourly),by=day_week]
mean.norain <- raw.data[rain==0,mean(ENTRIESn_hourly),by=day_week]
week_days <- c("MON","TUE","WED","THU","FRI","SAT","SUN")
week_days <- data.frame(week_days=factor(week_days,levels=week_days))
mean.mat <- cbind(as.numeric(mean.rain[order(mean.rain[,day_week]),V1]),as.numeric(mean.norain[order(mean.norain[,day_week]),V1]))
colnames(mean.mat) <- c("Rain","NoRain")
mean.mat <- data.frame(mean.mat)
mean.mat <- cbind(week_days,mean.mat)
ggplot(data=mean.mat,aes(x=week_days))+geom_line(aes(y=Rain,colour="Rain",group=1))+geom_line(aes(y=NoRain,colour="NoRain",group=1))+theme(legend.title=element_blank())+xlab("WeekDay")+ylab("Entries")



raw.data <- fread(input="turnstile_weather_v2.csv", header=TRUE)
data <- aggregate(raw.data[,.(ENTRIESn_hourly, latitude, longitude)], by=list(raw.data[,station]), FUN=mean)
ggmap(get_googlemap(center='new york ridgewood', zoom=11, maptype='roadmap'), extent='device') + 
  geom_point(data=data, aes(x=longitude,y=latitude),colour = 'blue', size=(data$ENTRIESn_hourly/800),alpha=0.5)



