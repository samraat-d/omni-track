function generateScholarship() {
    var name = document.getElementById("name").value;
    var age = document.getElementById("age").value;
    var dob = document.getElementById("dob").value;
    var gender = document.getElementById("gender").value;
    var course = document.getElementById("course").value;
    var reservation = document.getElementById("reservation").value;
    var enteredGPA = parseFloat(document.getElementById("gpa").value);
  
    // Hardcoded scholarship data
    var scholarships = [
      {
        name: "Huawei Scholarship for Excellence",
        criteria: {
          gpa: 9.5, // Adjusted GPA threshold
          financialNeed: true,
          fieldOfStudy: "Engineering",
        },
      },
      { 
        name: "DSW SC Scholarship",
        criteria: {
          gpa: 8, // Adjusted GPA threshold
          reservation: "SC",
        },
      },
      {
        name: "DSW ST Scholarship",
        criteria: {
          gpa: 7.5, // Adjusted GPA threshold
          reservation: "ST",
        },
      },
      {
        name: "DSW ST freeship",
        criteria: {
          gpa: 7.5, // Adjusted GPA threshold
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
  
    // Find matching scholarships
    var matchingScholarships = scholarships.filter(function(scholarship) {
      if (scholarship.criteria.gpa && enteredGPA >= scholarship.criteria.gpa) {
        // Check other criteria as needed
        return true;
      }
      return false;
    });
  
    // Display result
    displayResult(matchingScholarships);
  }
  
  function displayResult(matchingScholarships) {
    var resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<h2>Matching Scholarships:</h2><br><br>";
    
    if (matchingScholarships.length === 0) {
      resultDiv.innerHTML += "<p>No matching scholarships found.</p>";
    } else {
      matchingScholarships.forEach(function(scholarship) {
        resultDiv.innerHTML += "<p>Name: " + scholarship.name + "</p>";
        for (var criterion in scholarship.criteria) {
          resultDiv.innerHTML += "<p>" + criterion + ": " + scholarship.criteria[criterion] + "</p>";
        }
        resultDiv.innerHTML += "<br><hr><br><br>";
      });
    }
  }
  
  
  
