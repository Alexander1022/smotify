var forYou = window.sessionStorage.getItem("forYou")?.split(",") ?? [];
var forYouEdited = [];

function putInSes(string)
{
    forYou.push(string);
    sessionStorage.setItem('forYou', forYou); 
}

function getNotUnique()
{
    let sorted_arr = sessionStorage.getItem('forYou');
    let array = sorted_arr.split(",");

    var map = new Map();
    array.forEach(a => map.set(a, (map.get(a) || 0) + 1));
    array.filter(a => map.get(a) > 1);

    forYouEdited = [...new Set(array)];
}