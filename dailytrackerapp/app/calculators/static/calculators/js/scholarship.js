function generateScholarship() {
  var name = document.getElementById("name").value;
  var age = document.getElementById("age").value;
  var dob = document.getElementById("dob").value;
  var gender = document.getElementById("gender").value;
  var course = document.getElementById("course").value;
  var reservation = document.getElementById("reservation").value;
  var enteredGPA = parseFloat(document.getElementById("gpa").value);

  var scholarships = [
    {
      name: "Huawei Scholarship for Excellence",
      criteria: {
        gpa: 9.5, 
        financialNeed: true,
        fieldOfStudy: "Engineering",
      },
    },
    { 
      name: "DSW SC Scholarship",
      criteria: {
        gpa: 8, 
        reservation: "SC",
      },
    },
    {
      name: "DSW ST Scholarship",
      criteria: {
        gpa: 7.5, 
        reservation: "ST",
      },
    },
    {
      name: "DSW ST freeship",
      criteria: {
        gpa: 7.5, 
        reservation: "ST",
        financialNeed: true,
      },
    },
    {
      name: "DSW SC freeship",
      criteria: {
        gpa: 8,  
        reservation: "SC",
        financialNeed: true,
      },
    },
    {
      name: "LIG/ Free ship",
      criteria: {
        gpa: 8.2,
        reservation: "SC",
        financialNeed: true,
      },
    },
  ];

  var matchingScholarships = scholarships.filter(function(scholarship) {
    if (scholarship.criteria.gpa && enteredGPA >= scholarship.criteria.gpa) {
      return true;
    }
    return false;
  });

  displayResult(matchingScholarships);
}

function displayResult(matchingScholarships) {
  var resultContainer = document.getElementById("resultContainer");
  resultContainer.innerHTML = ""; // Clear previous results

  if (matchingScholarships.length === 0) {
    resultContainer.innerHTML += "<p>No matching scholarships found.</p>";
  } else {
    resultContainer.innerHTML += "<h2>Matching Scholarships:</h2><br>";
    matchingScholarships.forEach(function(scholarship) {
      resultContainer.innerHTML += "<p>Name: " + scholarship.name + "</p>";
      for (var criterion in scholarship.criteria) {
        resultContainer.innerHTML += "<p>" + criterion + ": " + scholarship.criteria[criterion] + "</p>";
      }
      resultContainer.innerHTML += "<br>";
    });
  }
}
