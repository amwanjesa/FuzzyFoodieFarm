
def doTheSearch(button):
    clear_output()
    # call from api
    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search?number=15&offset=0&query="
    url += searchterms.value +"&type=main+course&cuisine=" + cuisine.value
    recipes = unirest.get(url,
      headers={
        "X-Mashape-Key": "uI9T1GTt8nmshcUUWJOjq8TQNGBgp1P9Zffjsn7dAbkmTSDt1k",
        "Accept": "application/json"
      }
    )

    # present data properly
    testData = recipes.body
    testFrame = pd.DataFrame(testData['results'], columns=['id', 'title', 'readyInMinutes'])

    # fuzzify ratio
    degreeRatios = []
    ratios = testFrame.get('readyInMinutes')/int(time_available.value)
    for ratio in ratios:
        _, degreesRatio = fuzzyTime.member_of_function(ratio)
        degreeRatios.append(degreesRatio)

    degreeClusters = []
    # fuzzify activity
    for idRecipe in list(testFrame.id.values):
        _, clusters = cluster.testClustering(4, 1.5, str(idRecipe))
        degreeClusters.append(clusters)

    crisp_outputs = []
    for i in range(len(degreeRatios)):
        degreesRatio = degreeRatios[i]
        degreesClusters = degreeClusters[i]
        output = di.defuzzify(degreesRatio, degreesClusters, activities, activity.value)
        crisp_outputs.append(output)

    sortedIndices = heapq.nlargest(len(crisp_outputs), xrange(len(crisp_outputs)), key=crisp_outputs.__getitem__)[:5]
    rankedRecipes = testFrame.ix[sortedIndices]

    print rankedRecipes['title']
