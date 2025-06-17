import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlib

import os
from django.shortcuts import render
from django.conf import settings

DATA_CATEGORIES = {
    "Sales": "sales",
    "Students": "students",
    "Titanic": "titanic",
    "Flights": "flights",
    "Iris": "iris",
    "Tips": "tips",
    "Diamonds": "diamonds",
    "Planets": "planets",
    "Insurance": "insurance",
    "Weather": "weather"
}

def analyze_category(request):
    selected = None
    plot_url = None
    head = None

    if request.method == "POST":
        selected = request.POST.get("category")
        csv_file = request.FILES.get("csvfile")

        if selected and csv_file:
            df = pd.read_csv(csv_file)
            head = df.describe().to_html(classes="table table-striped")

            # Generate a plot
            plot_path = os.path.join(settings.BASE_DIR, "static", "analysis", "plot.png")
            plt.figure(figsize=(8, 5))
            try:
                # Basic plot logic (can be improved per category)
                # What does the user want to analyze?
                if selected == "Sales":
                    df['Sales'].plot(kind='bar', title='Sales Data')
                elif selected == "Students":
                    df['Scores'].plot(kind='line', title='Student Scores')
                elif selected == "Titanic":
                    print("Plotting Titanic data")
                    df['survived'].value_counts().plot(kind='pie', autopct='%1.1f%%', title='Titanic Survival')
                    plt.ylabel('')  # Hide the y-label for pie chart
                    plt.title('Titanic Survival Distribution')
                    plt.legend(title='Survived', loc='upper right')
                    plt.tight_layout()  # Adjust layout to prevent clipping
                    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular
                    
                elif selected == "Flights":
                    df['passengers'].plot(kind='line', title='Flight Passengers Over Time')
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.ylabel('Number of Passengers')
                    plt.xlabel('Flight Date')
                elif selected == "Iris":
                    df.plot.scatter(x='sepal_length', y='sepal_width', title='Iris Sepal Dimensions')
                elif selected == "Tips":
                    # Clean the table
                    df = df.dropna()

                    # Create data frame with analysis
                    plt.style.use('Solarize_Light2')
                    fig, graphs = plt.subplots(2,2, figsize=(20,20)) # graphs[0,0] 
                    graphs[0,0].scatter(df['total_bill'], df['tip'])
                    graphs[0,0].set_xlabel("Total Bill")
                    graphs[0,0].set_ylabel("Tip")
                    graphs[0,0].set_title("TotalBill vs Tip")

                    df_genderwise = df.groupby('sex')['tip'].mean().reset_index()
                    graphs[0,1].bar(df_genderwise['sex'],df_genderwise['tip'])
                    graphs[0,1].set_xlabel("Gender")
                    graphs[0,1].set_ylabel("Tip")
                    graphs[0,1].set_title("x vs Cube")

                    df_smoker = df.groupby('smoker')['tip'].mean().reset_index()
                    print(df_smoker)
                    graphs[1,0].bar(df_smoker['smoker'],df_smoker['tip'])
                    graphs[1,0].set_xlabel("smoker")
                    graphs[1,0].set_ylabel("Tip")
                    graphs[1,0].set_title("Smoker vs Tip")
                    fig.savefig("MatplotLibPractices.jpeg")


                elif selected == "Diamonds":
                    df['price'].plot(kind='hist', bins=30, title='Diamond Price Distribution')
                elif selected == "Planets":
                    df['mass'].plot(kind='scatter', y='orbital_period', title='Planet Mass vs Orbital Period')
                elif selected == "Insurance":
                    df['charges'].plot(kind='box', title='Insurance Charges Distribution')
                elif selected == "Weather":
                    df['temperature'].plot(kind='line', title='Weather Temperature Over Time')
                else:
                    # Default case for any other category
                    df.plot(kind='line', title='Data Analysis')
            except KeyError as e:
                print(f"KeyError: {e} - Check if the selected category has the required columns.")
                plt.text(0.5, 0.5, f"Error: {e}", horizontalalignment='center', verticalalignment='center', fontsize=12)
                plt.axis('off')  # Hide axes for error message
            # Save the plot
            #df.select_dtypes(include='number').hist(figsize=(10, 6))



            plt.tight_layout()
            plt.savefig(plot_path)
            plt.close()

            plot_url = "/static/analysis/plot.png"

    return render(request, "analyze.html", {
        "categories": list(DATA_CATEGORIES.keys()),
        "selected": selected,
        "head": head,
        "plot_url": plot_url,
    })
