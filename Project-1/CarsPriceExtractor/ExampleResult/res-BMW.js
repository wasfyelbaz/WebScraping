var data = [    {
        "name": "i/AHK/ALU/KLima/T\u00fcv Neu!Beschreibung Lesen! / BMW 116",
        "price": 4390,
        "mileage": 174900,
        "transmission": "Manual",
        "offer_type": "Used",
        "previous_owners": 3,
        "first_registration": "02/2009",
        "link": "https://www.autoscout24.com/offers/bmw-116-i-ahk-alu-klima-tuev-neu-beschreibung-lesen-gasoline-blue-0e816080-8408-440d-994a-38615fe452d2"
    },
    {
        "name": "i*Xenon*PDC*Sitzheizung*Klimaaut.* / BMW 116",
        "price": 4980,
        "mileage": 164145,
        "transmission": "Manual",
        "offer_type": "Used",
        "previous_owners": 2,
        "first_registration": "09/2008",
        "link": "https://www.autoscout24.com/offers/bmw-116-i-xenon-pdc-sitzheizung-klimaaut-gasoline-black-3f81cf5a-4802-4642-9681-3b9df1b45b2a"
    },
   ,
    {
        "name": "BMW 116 / D * GAR 12 MOIS * 5P * GPS * 1er prop *TOIT OUVR *",
        "price": 13990,
        "mileage": 36500,
        "transmission": "Manual",
        "offer_type": "Used",
        "previous_owners": 1,
        "first_registration": "08/2017",
        "link": "https://www.autoscout24.com/offers/bmw-116-i-5-tuerer-advantage-klima-pdc-freisprech-gasoline-black-94113c4e-5bd2-4436-a4e0-15d04bb794a5"
    }
]
resTitle = document.getElementById("res-title");
resTitle.innerHTML = 'res-BMW Results'
resTitle.setAttribute("align", "center");

function createCarLink(CAR) {
    var h3Tag = document.createElement("h3");
    var linkTag = document.createElement("a");
    linkTag.innerText = CAR.name;
    linkTag.setAttribute('href', CAR.link);
    h3Tag.innerHTML = '<a href="' + CAR.link + '">' + CAR.name + '</a> Price: ' + CAR.price;
    document.body.appendChild(h3Tag);
}

for (car of data) {
    createCarLink(car);
}
        