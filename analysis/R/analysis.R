library(dplyr)
library(ggplot2)

d <- read.csv("out.csv")

d <- d %>% mutate(real_net_time = (net_time - bd_time) - process_time, group = queries + results + rides)

t.test(d$process_time)

mean(d$process_time) + qnorm(0.975)*(sd(d$process_time)/sqrt(length(d$process_time)))
mean(d$process_time) - qnorm(0.975)*(sd(d$process_time)/sqrt(length(d$process_time)))

mean <- d %>% group_by(group) %>% 
              summarise(N = length(real_net_time), media = mean(real_net_time), sd = sd(real_net_time), se = sd/sqrt(N))

ggplot(mean, aes(x = as.factor(group), y = media)) + geom_point()+ geom_errorbar(aes(ymax = media +qnorm(0.975)*se, ymin = media - qnorm(0.975)*se))

media <- d %>% group_by(queries, results, rides) %>% 
                  summarise(net_mean = mean(real_net_time), process_mean = mean(process_time), bd_time = mean(bd_time), total_time_mean = mean(net_time))


 
