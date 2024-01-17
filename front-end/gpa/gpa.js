function inputmarks() 
{
 
    var n = document.getElementById("num").value;
    console.log(n);
    createmarks(n);
}

function createmarks(n){

    marksDiv = document.getElementById("main");

  for (let i=1;i<=n;i++)
  {
    let marksLabel = document.createElement('Label');
    marksDiv.appendChild(marksLabel);
    let marksLabeltxt = document.createTextNode("Enter the marks of subject " + i + " :");
    marksDiv.appendChild(marksLabeltxt);
    marksDiv.setAttribute('for', `marksval${i}`);

    let marksInput = document.createElement('input');
    marksDiv.appendChild(marksInput);
    marksInput.setAttribute('type', 'text');
    marksInput.setAttribute('id', `marksval${i}`);
    

    let gradeLabel = document.createElement('label');
    marksDiv.appendChild(gradeLabel);
    let gradeLabeltxt = document.createTextNode("Enter the grade of subject " + i + " :");
    marksDiv.appendChild(gradeLabeltxt);
    marksInput.setAttribute('for', `gradeval${i}`);

    let gradeInput = document.createElement('input');
    marksDiv.appendChild(gradeInput);
    gradeInput.setAttribute('type', 'text');
    gradeInput.setAttribute('id', `gradeval${i}`);
    

    let creditLabel = document.createElement('label');
    marksDiv.appendChild(creditLabel);
    let creditLabeltxt = document.createTextNode("Enter credits of subject " + i + " :");
    marksDiv.appendChild(creditLabeltxt);
    marksInput.setAttribute('for', `creditval${i}`);

    let creditInput=document.createElement('input');
    marksDiv.appendChild(creditInput);
    creditInput.setAttribute('type','text');
    creditInput.setAttribute('id',`creditval${i}`);
    marksDiv.appendChild(document.createElement('br')); 
    marksDiv.appendChild(document.createElement('br')); 
  }
}

function gpacal() 
 {
    let totalCredits = 0;
    let totalGradePoints = 0;

    let grades = [];
    let credits = [];

    for (let i = 1; i <= n; i++) {
        
        let grade = parseFloat(document.getElementById(`grade${i}`).value);
        let credit = parseFloat(document.getElementById(`credit${i}`).value);

       
        grades.push(grade);
        credits.push(credit);
    }

    for (let i=0;i<n;i++) 
    {
        totalGradePoints += grades[i] * credits[i];
        totalCredits += credits[i];
    }

    const cgpa = totalGradePoints / totalCredits;

    if (!isNaN(cgpa)) 
    {
        document.getElementById('result').innerHTML = `Your CGPA is: ${cgpa.toFixed(2)}`;
    } 
    else 
    {
        document.getElementById('result').innerHTML = 'Please enter valid grades and credits.';
    }
}
