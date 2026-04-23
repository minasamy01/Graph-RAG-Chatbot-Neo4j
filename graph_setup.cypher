
/* =========================
   ELEMENTS
========================= */

MERGE (:Element {symbol:"C"}) ON CREATE SET name="Carbon";
MERGE (:Element {symbol:"H"}) ON CREATE SET name="Hydrogen";
MERGE (:Element {symbol:"O"}) ON CREATE SET name="Oxygen";


/* =========================
   REACTIONS
========================= */

MERGE (:Reaction {equation:"C + 4H -> CH4"});
MERGE (:Reaction {equation:"C + O2 -> CO2"});


/* =========================
   COMPOUNDS
========================= */

MERGE (:Compound {name:"Methane", formula:"CH4"});
MERGE (:Compound {name:"Carbon Dioxide", formula:"CO2"});


/* =========================
   METHANE RELATIONS
========================= */

MATCH (c:Element {symbol:"C"}),
      (h:Element {symbol:"H"}),
      (r:Reaction {equation:"C + 4H -> CH4"}),
      (m:Compound {formula:"CH4"})
MERGE (c)-[:REACTANT {ratio:"1"}]->(r)
MERGE (h)-[:REACTANT {ratio:"4"}]->(r)
MERGE (r)-[:PRODUCT]->(m);


/* =========================
   CARBON DIOXIDE RELATIONS
========================= */

MATCH (c:Element {symbol:"C"}),
      (o:Element {symbol:"O"}),
      (r:Reaction {equation:"C + O2 -> CO2"}),
      (co2:Compound {formula:"CO2"})
MERGE (c)-[:REACTANT {ratio:"1"}]->(r)
MERGE (o)-[:REACTANT {ratio:"2"}]->(r)
MERGE (r)-[:PRODUCT]->(co2);


/* =========================
   DRUGS
========================= */

MERGE (:Drug {name:"Paracetamol"});
MERGE (:Drug {name:"Aspirin"});


/* =========================
   DRUG RELATIONS
========================= */

MATCH (m:Compound {formula:"CH4"}), 
      (p:Drug {name:"Paracetamol"})
MERGE (m)-[:USED_IN]->(p);

MATCH (co2:Compound {formula:"CO2"}), 
      (a:Drug {name:"Aspirin"})
MERGE (co2)-[:USED_IN]->(a);


/* =========================
   DISEASES
========================= */

MERGE (:Disease {name:"Fever"});
MERGE (:Disease {name:"Headache"});


/* =========================
   TREATS
========================= */

MATCH (p:Drug {name:"Paracetamol"}), 
      (d:Disease {name:"Fever"})
MERGE (p)-[:TREATS]->(d);

MATCH (p:Drug {name:"Aspirin"}), 
      (d:Disease {name:"Headache"})
MERGE (p)-[:TREATS]->(d);


/* =========================
   ORGANISMS
========================= */

MERGE (:Organism {type:"Human"});
MERGE (:Organism {type:"Mouse"});


/* =========================
   AFFECTS
========================= */

MATCH (d:Disease {name:"Fever"}),
      (h:Organism {type:"Human"})
MERGE (d)-[:AFFECTS]->(h);

MATCH (d:Disease {name:"Headache"}),
      (h:Organism {type:"Mouse"})
MERGE (d)-[:AFFECTS]->(h);

MATCH (d:Disease {name:"Headache"}),
      (h:Organism {type:"Human"})
MERGE (d)-[:AFFECTS]->(h);


/* =========================
   VIEW GRAPH
========================= */

MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m;