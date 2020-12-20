#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
# Allen (github: alc00)

library(shiny)

# Define server logic
shinyServer(function(input, output) {
    
    # Create Reactive Data Frame
        global <- reactiveValues(
            main_data = data.frame()
        )
    
    # Compute for Remaining Life and Working Years
        remaining_total_years <- reactive({input$life_expectancy-input$current_age})
        remaining_working_years <- reactive({input$retirement_age-input$current_age})
        
    # Create a vector based on total years and remaining years
        time_series <- reactive({1:remaining_total_years()})
        
    # Create a vector for total non-investment income
        revenue_work_f <- reactive({
            revenue_work <- c()
            for (i in time_series()) {
                revenue_work_year <- input$working_income * (1+((input$working_income_increase/100)/1))^(1*(i-1))
                revenue_work_year <- ifelse(i <= remaining_working_years(), revenue_work_year, 0)
                revenue_work <- append(revenue_work, revenue_work_year)
            }
            return(round(revenue_work,2))
                })
    
    # Create a vector for total living expenses
        living_costs_f <- reactive({
            living_costs <- c()
            for (i in time_series()) {
                living_costs_year <- input$living_costs * (1+(((input$living_costs_increase+input$inflation_rate)/100)/1))^(1*(i-1))
                living_costs <- append(living_costs, living_costs_year)
            }
            return(round(living_costs,2))
        })

    # Create a vector for investment accumulation
    asset_value_f <- reactive({
        asset_value <- c()
        asset_income <-c()
        asset_value_year_start <- input$asset_value
        for (i in time_series()) {
            asset_value_year_income <- asset_value_year_start * (input$annual_yield_assets/100)
            asset_value_year_end <- asset_value_year_start + asset_value_year_income + (revenue_work_f()[i]-living_costs_f()[i])
            asset_value <- append(asset_value, asset_value_year_end)
            asset_income <- append(asset_income,asset_value_year_income)
            
            asset_value_year_start <- asset_value_year_end
        }
        return(round(asset_value,2))
    }) 

    # Create a vector for investment income
    asset_income_f <- reactive({
        asset_value <- c()
        asset_income <-c()
        asset_value_year_start <- input$asset_value
        for (i in time_series()) {
            asset_value_year_income <- asset_value_year_start * (input$annual_yield_assets/100)
            asset_value_year_end <- asset_value_year_start + asset_value_year_income + (revenue_work_f()[i]-living_costs_f()[i])
            asset_value <- append(asset_value, asset_value_year_end)
            asset_income <- append(asset_income,asset_value_year_income)
            
            asset_value_year_start <- asset_value_year_end
        }
        return(round(asset_income,2))
    })    
        
    # Combine Calculated Data
        
        df_sel <- reactive({
            total_income <- revenue_work_f() + asset_income_f()
            net_savings <- total_income - living_costs_f()
            age <- time_series()+input$current_age
            
            global$main_data = data.frame(year = time_series(), 
                                          age = age,
                                          active_income = revenue_work_f(), 
                                          living_costs = living_costs_f(),
                                          asset_income = asset_income_f(),
                                          total_income = total_income,
                                          net_savings = net_savings,
                                          asset_value = asset_value_f()
                                          )
            
            return(global$main_data)
        })
        
    # Create Plot 1
        
        plot_sel_1 <- reactive({
            plot(x=df_sel()$age, 
                 y=df_sel()$total_income, 
                 type = "l", 
                 col = "green",
                 xlab = "Age",
                 ylab = "Currency Value",
                 main = "Financial Summary - Income and Expenses"
                 )
            lines(x=df_sel()$age, y=df_sel()$living_costs, col = "red")

            legend(x = 0,
                   y = 0,
                   legend = c("Total Income", "Total Living Costs"), 
                   col = c("green", "red"),
                   lty = 1:2,
                   cex = 0.8
            )
        })
        
        
        
    # Create Plot 2
        
        plot_sel_2 <- reactive({
            plot(x=df_sel()$age, 
                 y=df_sel()$asset_value, 
                 type = "l", 
                 col = "blue",
                 xlab = "Age",
                 ylab = "Currency Value",
                 main = "Financial Summary - Net Worth"
            )
            lines(x=df_sel()$age, y=df_sel()$age-df_sel()$age, col = "gray")
        })
        
    output$plot1 <- renderPlot(plot_sel_1())
    output$plot2 <- renderPlot(plot_sel_2())
    
    output$active_income <- renderText(format(sum(df_sel()$active_income), nsmall=2, big.mark=",", scientific=F))
    output$asset_income <- renderText(format(sum(df_sel()$asset_income), nsmall=2, big.mark=",", scientific=F))
    output$total_income <- renderText(format(sum(df_sel()$total_income), nsmall=2, big.mark=",", scientific=F))
    output$living_costs <- renderText(format(sum(df_sel()$living_costs), nsmall=2, big.mark=",", scientific=F))
    output$asset_value <- renderText(format(sum(df_sel()$net_savings), nsmall=2, big.mark=",", scientific=F))
    output$breakeven_age <- renderText(max(df_sel()[df_sel()$asset_value >=0, "age"]))
    
    output$comp_table <- renderDataTable(data.frame(
                                            Year = df_sel()$year,
                                            Ending_Age = df_sel()$age,
                                            Active_Income = format(df_sel()$active_income, nsmall=2, big.mark=",", scientific=F),
                                            Investment_Income = format(df_sel()$asset_income, nsmall=2, big.mark=",", scientific=F),
                                            Total_Income = format(df_sel()$total_income, nsmall=2, big.mark=",", scientific=F),
                                            Expenses = format(df_sel()$living_costs, nsmall=2, big.mark=",", scientific=F),
                                            Net_Savings = format(df_sel()$net_savings, nsmall=2, big.mark=",", scientific=F),
                                            Net_Worth = format(df_sel()$asset_value, nsmall=2, big.mark=",", scientific=F)
                                            )
                                        )
})
