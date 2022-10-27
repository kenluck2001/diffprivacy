const sylvester = require("sylvester");

const hadamard = (l) => {
    var H = $M([
      [1, 1],
      [1, -1]
    ]);
    for (let i = 1; i < Math.log2(l); i++) {
        var posy = H.augment(H).transpose()
        var negy = H.augment(H.x(-1)).transpose()
        var hmat = posy.augment(negy)
        H = hmat;
    }
    return H;
}

const random = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

const range = (start, stop, step) => {
    var a = [start], b = start;
    while (b < stop) {
        a.push(b += step || 1);
    }
    return a;
}

const sample = (min, max, epilson) => {
    let prob = Math.exp(epilson) / (1 + Math.exp(epilson)); 
    if (Math.random() <= prob)
    {
        return min
    }
    return max;
}

const hashCode = (s) => {
    let h = 0;
    let str = s.toLowerCase();
    let n = str.length;
    for(let i = 0; i < n; i++)
    { 
        var char = str.charCodeAt(i) - 97 + 1;
        h = h + (char * Math.pow(26, (n - i - 1)));
    }
    return h;
}

const hash = (d, k, m) => {
    let degree = 3; // 3-wise indeopendent hash function
    let dval = hashCode(d);
    let rmatrix = sylvester.Matrix.Random(k, degree - 1);
    //let rindex = random(0, k-1);
    let rindex = random(1, k);
    let rvector = rmatrix.row(rindex);
    let hequation = range(0, k-1, 1).map(function(x) { return Math.pow(dval, x) });
    let hequationVec = $V(hequation);
    let hashval = Math.round(hequationVec.dot(rvector)) % m;
    return [hashval, rindex];
}

const hash2 = (d, k, rindex, m) => {
    let degree = 3; // 3-wise indeopendent hash function
    let dval = hashCode(d);
    let rmatrix = sylvester.Matrix.Random(k, degree - 1);
    let rvector = rmatrix.row(rindex);
    let hequation = range(0, k-1, 1).map(function(x) { return Math.pow(dval, x) });
    let hequationVec = $V(hequation);
    let hashval = Math.round(hequationVec.dot(rvector)) % m;
    return hashval;
}

const Aclient_HCMS = (d, m, k, epilson) => {
    let v = sylvester.Vector.Zero(m).elements;
    let [hindex, jindex] = hash(d, k, m);
    v[hindex] = 1;
    let w = hadamard(m).x($V(v));
    let prob = Math.exp(epilson) / (1 + Math.exp(epilson)); 
    let b = -1;
    if (Math.random() <= prob)
    {
        b = 1;
    }
    let lindex = random(2, Math.floor(Math.sqrt(m)) );
    lindex = Math.pow(lindex, 2);
    let hatw = b * w.elements[lindex];
    return [hatw, jindex, lindex];
}

const Asketch_HCMS = (dtuple_list, m, k, epilson) => {
    let cepilson = (Math.exp(epilson) + 1) / (Math.exp(epilson) - 1); 
    let MHmat = sylvester.Matrix.Zero(k, m).elements;
    for (let i = 0; i < dtuple_list.length; i++) { 
        let hatw = dtuple_list[i].hatw;
        let jindex = dtuple_list[i].jindex;
        let lindex = dtuple_list[i].lindex;

        if (!isNaN(hatw) || (typeof xhat !== 'undefined'))
        {
            let xhat = k * cepilson * hatw;
            console.log ( "hatw: " + hatw + ", jindex: " + jindex + ", lindex: " + lindex);


            try {

                if(typeof MHmat[jindex][lindex] !== 'undefined')
                {
                    MHmat[jindex][lindex] = MHmat[jindex][lindex] + xhat;
                }
            }
            catch(err) {
              console.log(err.message);
            }

        }

    }
    MHmat = $M(MHmat).x(hadamard(m).transpose());
    return MHmat;
}

const Aserver = (d, n, m, k, MHmat, epilson) => {
    MHmat = MHmat.elements;
    let summation = 0;
    for (let l = 1; l < k; l++) { 
        let hashval = hash2(d, k, l, m);
        summation = summation + MHmat[l][hashval];
    }
    let avg = summation / k;
    let res =  (m / (m - 1)) * ( avg - (n / m)); 
    return res;
}


/////////////////////////////////////////////
/////////////////////////////////////////////
/////////////////////////////////////////////

let m = 1024; 
let k = 64; 
let epilson = 2;

let votes = ["ken", "ken", "ken", "ken", "ken", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam", "sam"]
let uniqvotes = ["ken", "sam", "dan"]
dlist = []
for (let ind = 0; ind < votes.length; ind++) { 
    let dv = votes[ind];
    let [hatw, jindex, lindex] = Aclient_HCMS(dv, m, k, epilson);
    let clist = {
        "hatw": hatw,
        "jindex": jindex,
        "lindex": lindex,
    };
    dlist.push(clist);
}

let MHmatx = Asketch_HCMS(dlist, m, k, epilson );
for (let ind = 0; ind < uniqvotes.length; ind++) { 
    let dv = uniqvotes[ind];
    let freq = Aserver(dv, votes.length, m, k, MHmatx, epilson);
    console.log ("vote: " + dv + ", freq: " + freq);
}

