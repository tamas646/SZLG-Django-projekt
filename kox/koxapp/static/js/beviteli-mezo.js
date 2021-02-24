function tápanyag_átváltás(){

    var kaloria,zsir,feherje,szenhidrat;

    kaloria = document.getElementById("kcal");
    zsir = document.getElementById("fat");
    feherje = document.getElementById("prot");
    szenhidrat = document.getElementById("carb");

    kaloria.value = ((zsir.value*9)+(feherje.value*4)+(szenhidrat.value*4));
    return kaloria;
}
