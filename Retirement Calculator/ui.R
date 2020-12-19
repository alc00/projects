#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
# Allen (github: alc00)

library(shiny)

# Define UI for application
shinyUI(fluidPage(

    # Application title
    titlePanel("Retirement Calculator"),

    # Sidebar with the inputs and sliders regarding the user's profile and financial expectations
    sidebarLayout(
        sidebarPanel(
            sliderInput("current_age",
                        "Current Age:",
                        min = 0,
                        max = 120,
                        value = 25),
            sliderInput("life_expectancy",
                        "Estimated Life Expectancy:",
                        min = 0,
                        max = 120,
                        value = 100),
            sliderInput("retirement_age",
                        "Planned Retirement Age (i.e. Age when you plan to stop working):",
                        min = 0,
                        max = 120,
                        value = 60),
            numericInput("asset_value",
                         "Current Asset Value (e.g. savings, stocks, real estate):",
                         value = 0),
            sliderInput("annual_yield_assets",
                        "Estimated Annual Net Yield from Assets (e.g. interest, rent, capital appreciation):",
                        min = 0,
                        max = 100,
                        value = 4,
                        post = "%"),
            numericInput("working_income",
                         "Current Non-Investment Net Income (e.g. salary, freelance income, business):",
                         value = 0),
            sliderInput("working_income_increase",
                        "Estimated Annual Increase in Non-Investment Net Income (e.g. salary increases)",
                        min = 0,
                        max = 100,
                        value = 5,
                        post = "%"),
            numericInput("living_costs",
                         "Current Living Expenses (i.e. annual budget for expenses):",
                         value = 0),
            sliderInput("living_costs_increase",
                        "Estimated Annual Increase in Lifestyle Costs (e.g. buying more stuff)",
                        min = 0,
                        max = 100,
                        value = 0,
                        post = "%"),
            sliderInput("inflation_rate",
                        "Inflation Rate (e.g. price increase for the stuff you currently buy):",
                        min = 0,
                        max = 100,
                        value = 2,
                        post = "%")
        ),

        mainPanel(
            # Plot Outputs
            h3("Financial Pathway - Income and Expenses"),
                plotOutput("plot1"),
            
            h3("Financial Pathway - Net Worth"),
                plotOutput("plot2"),
            
            # Numeric Outputs
            h3("Summary"),
            h4("Lifetime Active Income"),
            textOutput("active_income"),
            
            h4("Lifetime Investment Income"),
            textOutput("asset_income"),
            
            h4("Lifetime Total Income"),
            textOutput("total_income"),
            
            h4("Lifetime Living Expenses"),
            textOutput("living_costs"),
            
            h4("Final Asset Value"),
            textOutput("asset_value"),
            
            h4("Max Living Age with Positive Net Worth"),
            textOutput("breakeven_age")
            
        )
    )
))
