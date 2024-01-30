let gradeval$;
let creditval$;
let marksval$;
let n1; // Declare n1 here to avoid the undefined error

function inputmarks() {
    var n = document.getElementById("num").value;
    console.log(n);
    createmarks(n);
}

function createmarks(n) {
    let marksDiv = document.getElementById("gpaForm1");

    for (let i = 1; i <= n; i++) {
        let marksLabel = document.createElement('label');
        marksDiv.appendChild(marksLabel);
        let marksLabeltxt = document.createTextNode("Enter the marks of subject " + i + " :");
        marksLabel.appendChild(marksLabeltxt);
        marksLabel.setAttribute('for', `marksval${i}`);

        let marksInput = document.createElement('input');
        marksDiv.appendChild(marksInput);
        marksInput.setAttribute('type', 'text');
        marksInput.setAttribute('id', `marksval${i}`);
        marksDiv.appendChild(document.createElement('br'));
        marksDiv.appendChild(document.createElement('br'));

        let gradeLabel = document.createElement('label');
        marksDiv.appendChild(gradeLabel);
        let gradeLabeltxt = document.createTextNode("Enter the grade of subject  " + i + "   :");
        gradeLabel.appendChild(gradeLabeltxt);
        gradeLabel.setAttribute('for', `gradeval${i}`);
       

        let gradeInput = document.createElement('input');
        marksDiv.appendChild(gradeInput);
        gradeInput.setAttribute('type', 'text');
        gradeInput.setAttribute('id', `gradeval${i}`);
        marksDiv.appendChild(document.createElement('br'));
        marksDiv.appendChild(document.createElement('br'));

        let creditLabel = document.createElement('label');
        marksDiv.appendChild(creditLabel);
        let creditLabeltxt = document.createTextNode("Enter the credits of subject " + i + ":");
        creditLabel.appendChild(creditLabeltxt);
        creditLabel.setAttribute('for', `creditval${i}`);
       

        let creditInput = document.createElement('input');
        marksDiv.appendChild(creditInput);
        creditInput.setAttribute('type', 'text');
        creditInput.setAttribute('id', `creditval${i}`);
        marksDiv.appendChild(document.createElement('br'));
        marksDiv.appendChild(document.createElement('br'));
        marksDiv.appendChild(document.createElement('br'));
        marksDiv.appendChild(document.createElement('br'));
    }
}

function gpacal() {
    let totalCredits = 0;
    let totalGradePoints = 0;

    n1 = document.getElementById("num").value; 

    let grades = [];
    let credits = [];

    for (let i = 1; i <= n1; i++) {
        let grade = parseFloat(document.getElementById(`gradeval${i}`).value);
        let credit = parseFloat(document.getElementById(`creditval${i}`).value);

        grades.push(grade);
        credits.push(credit);
    }

    for (let i = 0; i < n1; i++) {
        totalGradePoints += grades[i] * credits[i];
        totalCredits += credits[i];
    }

    const cgpa = totalGradePoints / totalCredits;

    if (!isNaN(cgpa)) {
        document.getElementById("result").innerHTML = `Your CGPA is: ${cgpa.toFixed(2)}`;
    } else {
        document.getElementById("result").innerHTML = 'Please enter valid grades and credits.';
    }
}
