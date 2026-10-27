// Searchable product field: a single text input that filters the list below it while typing.
// Markup: <div class="product-search"> <input class="product-search-input"> <ul class="product-search-menu">
//         with <li class="product-search-option"> per product and optional <li class="product-search-header"> per group
// The input value is the chosen product name; anything not in the list is marked invalid, so forms cannot submit it.
(function () {
  // Lowercase, strip accents (ă â î ș ț ...) and collapse punctuation/whitespace into single spaces
  function normalizeText(text) {
    return text
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, ' ')
      .trim();
  }

  function setup(root) {
    var input = root.querySelector('.product-search-input');
    var menu = root.querySelector('.product-search-menu');
    var options = Array.from(menu.querySelectorAll('.product-search-option'));
    var headers = Array.from(menu.querySelectorAll('.product-search-header'));
    var noResults = document.createElement('li');
    noResults.className = 'product-search-empty';
    menu.appendChild(noResults);

    var names = {};
    options.forEach(function (option, index) {
      option.id = input.id + '-option-' + index;
      option.setAttribute('role', 'option');
      option.dataset.search = normalizeText(option.textContent);
      names[option.textContent.trim()] = true;
    });

    var active = null;

    function visibleOptions() {
      return options.filter(function (option) { return !option.hidden; });
    }

    function setActive(option) {
      if (active) {
        active.classList.remove('active');
      }
      active = option;
      if (active) {
        active.classList.add('active');
        input.setAttribute('aria-activedescendant', active.id);
        active.scrollIntoView({block: 'nearest'});
      } else {
        input.removeAttribute('aria-activedescendant');
      }
    }

    function filter() {
      var query = normalizeText(input.value);
      options.forEach(function (option) {
        option.hidden = !option.dataset.search.includes(query);
      });
      // a group header is shown only while one of its products is
      headers.forEach(function (header) {
        var next = header.nextElementSibling;
        var hasVisible = false;
        while (next && next.classList.contains('product-search-option')) {
          hasVisible = hasVisible || !next.hidden;
          next = next.nextElementSibling;
        }
        header.hidden = !hasVisible;
      });

      var visible = visibleOptions();
      noResults.hidden = visible.length > 0;
      noResults.textContent = (root.dataset.noneResultsText || '').replace('{0}', input.value);
      setActive(visible[0] || null);
    }

    function open() {
      filter();
      menu.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    }

    function close() {
      menu.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      setActive(null);
    }

    function validate() {
      var valid = input.value === '' || names[input.value];
      input.setCustomValidity(valid ? '' : 'Alege un produs din lista');
    }

    function choose(option) {
      input.value = option.textContent.trim();
      validate();
      close();
      input.dispatchEvent(new CustomEvent('product-chosen', {bubbles: true}));
    }

    input.addEventListener('focus', open);
    input.addEventListener('click', open);
    input.addEventListener('input', function () {
      validate();
      open();
    });

    input.addEventListener('keydown', function (event) {
      var visible = visibleOptions();
      var index = visible.indexOf(active);

      if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
        event.preventDefault();
        if (menu.hidden) {
          open();
          return;
        }
        var step = event.key === 'ArrowDown' ? 1 : -1;
        setActive(visible[Math.min(Math.max(index + step, 0), visible.length - 1)] || null);
      } else if (event.key === 'Enter' && !menu.hidden && active) {
        event.preventDefault();
        event.stopPropagation();
        choose(active);
      } else if (event.key === 'Escape') {
        close();
      }
    });

    // mousedown instead of click, so the input does not lose focus before the choice is made
    menu.addEventListener('mousedown', function (event) {
      event.preventDefault();
      var option = event.target.closest('.product-search-option');
      if (option) {
        choose(option);
      }
    });

    input.addEventListener('blur', function () {
      // typing the exact name with different case/accents still counts as choosing it
      if (input.value && !names[input.value]) {
        var query = normalizeText(input.value);
        var match = options.find(function (option) { return option.dataset.search === query; });
        if (match) {
          input.value = match.textContent.trim();
        }
      }
      validate();
      close();
    });

    close();
  }

  document.querySelectorAll('.product-search').forEach(setup);
})();
