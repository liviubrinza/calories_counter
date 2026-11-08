// Barcode scan button: takes a photo with the phone camera, sends it to the server to read the barcode
// and look the product up, then opens a product modal with the found values filled in.
// Markup: <button data-barcode-scan="{{ url_for('scan_product') }}"
//                 data-modal="#modal" data-form="#form" data-field-prefix="new-product-"
//                 data-alerts="#alerts" data-info="#info" [data-focus="#field"]>
// The fields are <prefix>name, <prefix>calories, <prefix>protein, <prefix>fats, <prefix>carbs.
// The photo is only sent to read its barcode and is not kept anywhere.
(function () {
  const fields = ['name', 'calories', 'protein', 'fats', 'carbs'];

  function showError(alerts, message) {
    const alert = $('<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
      '<i class="fa fa-exclamation-circle alert-icon" aria-hidden="true"></i><span></span>' +
      '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>');
    alert.find('span').first().text(message);
    $(alerts).empty().append(alert);
  }

  function setBusy(button, busy) {
    button.disabled = busy;
    button.querySelector('i').className = busy ? 'fa fa-spinner fa-spin' : 'fa fa-camera';
    button.querySelector('span').textContent = busy ? 'Se citeste...' : 'Poza';
  }

  function setup(button) {
    const options = button.dataset;
    const modal = $(options.modal);
    const info = document.querySelector(options.info);
    let prefilled = false;

    // opens the camera directly on phones, a file picker elsewhere
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/*';
    input.setAttribute('capture', 'environment');
    input.className = 'd-none';
    button.after(input);

    button.addEventListener('click', function () {
      input.click();
    });

    input.addEventListener('change', function () {
      const photo = input.files[0];
      if (!photo) return;

      const data = new FormData();
      data.append('photo', photo);
      // clear the input so the same photo is not kept around and a new one can be taken
      input.value = '';

      $(options.alerts).empty();
      setBusy(button, true);

      fetch(options.barcodeScan, { method: 'POST', body: data })
        .then(function (response) {
          if (response.status === 413) return { error: 'The photo is too large' };
          return response.json();
        })
        .then(function (result) {
          if (result.error) {
            showError(options.alerts, result.error);
            return;
          }

          const form = document.querySelector(options.form);
          form.reset();
          // missing values stay empty, so they have to be filled in by hand
          fields.forEach(function (key) {
            const value = result.product[key];
            document.getElementById(options.fieldPrefix + key).value = value === null ? '' : value;
          });
          info.textContent = 'Cod de bare ' + result.barcode + ' - verifica valorile inainte de a adauga produsul.';
          info.classList.remove('d-none');
          prefilled = true;
          modal.modal('show');
        })
        .catch(function () {
          showError(options.alerts, 'Error encountered while sending the photo');
        })
        .finally(function () {
          setBusy(button, false);
        });
    });

    if (options.focus) {
      // registered after the page's own focus handler, so it wins for scanned products
      modal.on('shown.bs.modal', function () {
        if (prefilled) $(options.focus).trigger('focus');
      });
    }

    // a scanned product should not linger in the form when it is opened normally afterwards
    modal.on('hidden.bs.modal', function () {
      if (!prefilled) return;
      document.querySelector(options.form).reset();
      info.classList.add('d-none');
      prefilled = false;
    });
  }

  document.querySelectorAll('[data-barcode-scan]').forEach(setup);
})();
