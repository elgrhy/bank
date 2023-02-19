from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# Load and preprocess the customer data
customer_data = pd.read_csv('recommend/data/customer_data.csv').dropna().drop_duplicates()

# Train the clustering algorithm to group customers
kmeans = KMeans(n_clusters=5).fit(customer_data[['income', 'expenses', 'debt']])

# Train the regression algorithm to predict future income
regression = LinearRegression().fit(customer_data[['age', 'income', 'savings']], customer_data[['income']])

@csrf_exempt
def home(request):
    if request.method == 'POST':
        # Parse customer data from the request
        age = int(request.POST.get('age'))
        income = int(request.POST.get('income'))
        expenses = int(request.POST.get('expenses'))
        debt = int(request.POST.get('debt'))
        savings = int(request.POST.get('savings'))
        customer_data = pd.DataFrame({'age': [age], 'income': [income], 'expenses': [expenses], 'debt': [debt], 'savings': [savings]})

        # Use the clustering algorithm to group the customer
        cluster = kmeans.predict(customer_data[['income', 'expenses', 'debt']])[0]

        # Use the regression algorithm to predict the customer's future income
        predicted_income = regression.predict(customer_data[['age', 'income', 'savings']])[0][0]

        # Use nudge theory to generate personalized recommendations
        recommendations = []
        if cluster == 0:
            recommendations.append('Consider investing in a diversified portfolio to increase your returns.')
        elif cluster == 1:
            recommendations.append('Pay down high-interest debt to reduce your interest payments.')
        elif cluster == 2:
            recommendations.append('Take advantage of tax-advantaged retirement accounts to save for the future.')
        elif cluster == 3:
            recommendations.append('Explore alternative sources of income, such as freelancing or consulting.')
        elif cluster == 4:
            recommendations.append('Consider refinancing your mortgage to lower your monthly payments.')

        # Use nudges to encourage specific behaviors
        nudges = []
        if predicted_income < income:
            nudges.append('You are on track to earn less than you are now. Consider ways to increase your income, such as taking on additional responsibilities at work or pursuing a higher-paying job.')
        if savings < income:
            nudges.append('You are saving less than you are earning. Consider increasing your savings rate to ensure a more secure financial future.')

        return render(request, 'index.html', {'recommendations': recommendations, 'nudges': nudges})

    return render(request, 'index.html')
