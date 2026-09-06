document.addEventListener('DOMContentLoaded', function () {
  // Toast notification function
  function showToast(message, type = 'success') {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.id = 'toast-container';
      document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // Update navbar cart badge
  function updateCartBadge(count, total) {
    const badge = document.getElementById('cart-badge-count');
    if (badge) {
      badge.textContent = count;
      badge.style.transform = 'scale(1.3)';
      setTimeout(() => {
        badge.style.transform = 'scale(1)';
        badge.style.transition = 'transform 0.2s ease';
      }, 200);
    }
  }

  // Handle AJAX Add to Cart
  document.querySelectorAll('.ajax-add-to-cart').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const url = this.action;
      const formData = new FormData(this);

      fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          showToast(data.message, 'success');
          updateCartBadge(data.cart_total_items, data.cart_total_price);
        } else {
          showToast(data.message || 'Error adding item to cart', 'error');
        }
      })
      .catch(err => {
        console.error('Cart add error:', err);
        this.submit(); // fallback to normal form POST
      });
    });
  });

  // Handle quantity adjustment (+/-) on product detail or cart
  document.querySelectorAll('.qty-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const input = this.parentElement.querySelector('.qty-input');
      if (!input) return;

      let currentVal = parseInt(input.value) || 1;
      if (this.classList.contains('qty-plus')) {
        const max = parseInt(input.getAttribute('max')) || 99;
        if (currentVal < max) input.value = currentVal + 1;
      } else if (this.classList.contains('qty-minus')) {
        const min = parseInt(input.getAttribute('min')) || 1;
        if (currentVal > min) input.value = currentVal - 1;
      }

      // Trigger change event if needed
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });

  // Auto-dismiss alert messages after 5 seconds
  document.querySelectorAll('.alert-close').forEach(closeBtn => {
    closeBtn.addEventListener('click', function () {
      this.parentElement.remove();
    });
  });
});
