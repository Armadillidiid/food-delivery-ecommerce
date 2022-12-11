import Cookies from "/static/node_modules/js-cookie/dist/js.cookie.mjs";
const csrftoken = Cookies.get("csrftoken");
const openHourOpenTime = document.querySelectorAll(".openHourOpenTime");
const openHourCloseTime = document.querySelectorAll(".openHourCloseTime");
const submitWeekdayBtn = document.querySelectorAll(".weekdaySubmitBtn");
const deleteWeekdayBtn = document.querySelectorAll(".deleteWeekdayBtn");

submitWeekdayBtn.forEach(function (btn, index) {
  btn.addEventListener("click", function () {
    console.log(btn);
    let url = "/create-update-open-hours/";
    let model_id = btn.dataset.model_id;
    let open_time = openHourOpenTime[index].value;
    let close_time = openHourCloseTime[index].value;
    let weekday = btn.dataset.weekday;
    let vendor = btn.dataset.vendor;
    console.log(url, model_id, open_time, close_time, weekday, vendor);
    updateCreateOpenHour(url, model_id, open_time, close_time, weekday, vendor);
  });
});

deleteWeekdayBtn.forEach(function (btn) {
  btn.addEventListener("click", function () {
    let url = "/delete-open-hours/";
    let model_id = btn.dataset.model_id;
    let weekday = btn.dataset.weekday;
    if ( model_id != '') {
      deleteOpenHour(url, model_id, weekday)
    }
  });
});

async function updateCreateOpenHour(
  url,
  model_id,
  open_time,
  close_time,
  weekday,
  vendor
) {
  console.log("Processing request");

  // Send request to server
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
    body: JSON.stringify({
      vendor: vendor,
      model_id: model_id,
      open_time: open_time,
      close_time: close_time,
      weekday: weekday,
    }),
  });

  // Read JSON response
  try {
    let data = await response.json();
    console.log(data);
    model_id = data["model_id"];
    weekday = data["weekday"];
    // Append saved object id to input
    appendDataAttribute(model_id, weekday);
    let showOpenHour = document.querySelector(`#showOpenHour${weekday}`);
    showOpenHour.innerHTML = `<span class="">${open_time} - ${close_time}</span>`;
  } catch (e) {
    console.log(e);
  }
}

async function deleteOpenHour(
  url,
  model_id,
  weekday,
) {
  console.log("Processing request");

  // Send request to server
  let response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    mode: "same-origin",
    body: JSON.stringify({
      model_id: model_id
    }),
  });

  // Read JSON response
  try {
    let data = await response.json();
    console.log(data);
    disableDeleteBtn(model_id, weekday)
    let showOpenHour = document.querySelector(`#showOpenHour${weekday}`)
    showOpenHour.innerHTML = `<span class="">None</span>`

  } catch (e) {
    console.log(e);
  }
}


function appendDataAttribute(model_id, weekday) {
  submitWeekdayBtn.forEach(function (btn, index) {
    if (btn.dataset.weekday == weekday) {
      btn.dataset.model_id = model_id;
    }
  });
  // Enable delete button
  deleteWeekdayBtn.forEach(function(btn) {
    if (btn.dataset.weekday == weekday) {
      btn.dataset.model_id = model_id
      btn.classList.remove('disabled')
    }
  })
}

function disableDeleteBtn(model_id, weekday) {
  deleteWeekdayBtn.forEach(function(btn) {
    if (btn.dataset.model_id == model_id) {
      btn.dataset.model_id = ''
      btn.classList.add('disabled')
    }
  })
  submitWeekdayBtn.forEach(function(btn) {
    if (btn.dataset.weekday == weekday) {
      btn.dataset.model_id = ''
    }
  })
}

const formInputs = document.querySelectorAll('#vendor-form div')
for (let input of formInputs) {
  console.log(input)
  input.classList.add('profile-form')
}

// Submit product form on clicking save
const productSubmitBtn = document.querySelector('#productSubmitBtn')
productSubmitBtn.addEventListener('click', function() {
  console.log('hreyyy')
  let productForm = document.querySelector('#productForm')
  productForm.submit()
})

// Submit category form on clicking save
const categorySubmitBtn = document.querySelector('#categorySubmitBtn')
categorySubmitBtn.addEventListener('click', function() {
  let categoryForm = document.querySelector('#categoryForm')
  categoryForm.submit()
})


// function convertTime12f(time) {
//   let hours = time.getHours()
//   let AmOrPm = hours >= 12 ? 'pm' : 'am';
//   let minute = time.getMinutes();
//   hours = (hours % 12) || 12;
//   let convertedTime = `${hours}:${minute} ${AmOrPm}`
//   console.log(convertedTime)
//   return convertedTime
// }