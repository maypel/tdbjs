console.log("bonjour");
        
$.ajax({
    url: "/api/news",
    success: display_news
});

console.log("Au revoir");
        
function display_news(result) {
    console.log("Résultat de la requête :", result);
    news_data = result["data"];
    console.log(news_data["articles"].length);
    console.log(news_data["keywords"][0]["mot"]);
}