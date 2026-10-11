// QC Lab Manager - PWA Auto-Update Detection & Notification System
(function() {
  'use strict';

  if (!('serviceWorker' in navigator)) {
    console.log('[PWA Updater] Service workers are not supported by this browser.');
    return;
  }

  let swRegistration = null;
  let waitingWorker = null;
  let updateToast = null;
  let isUpdating = false;

  // 1. Create and inject the update prompt banner into DOM
  function createUpdateToast() {
    if (document.getElementById('pwa-update-toast')) {
      return document.getElementById('pwa-update-toast');
    }

    const toast = document.createElement('div');
    toast.id = 'pwa-update-toast';
    toast.setAttribute('role', 'alert');
    toast.style.cssText = `
      position: fixed;
      bottom: 1.25rem;
      right: 1.25rem;
      z-index: 999999;
      max-width: 24rem;
      width: calc(100% - 2.5rem);
      background: rgba(15, 23, 42, 0.96);
      color: #ffffff;
      padding: 1rem;
      border-radius: 1rem;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.6), 0 0 20px rgba(59, 130, 246, 0.35);
      border: 1px solid rgba(59, 130, 246, 0.45);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      opacity: 0;
      transform: translateY(1.5rem) scale(0.96);
      transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
      pointer-events: none;
    `;

    toast.innerHTML = `
      <div style="display: flex; align-items: flex-start; gap: 0.85rem;">
        <div style="width: 2.5rem; height: 2.5rem; border-radius: 0.75rem; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); display: flex; align-items: center; justify-content: center; flex-shrink: 0; color: #60a5fa; font-size: 1.15rem;">
          <i class="fas fa-arrows-rotate fa-spin" style="--fa-animation-duration: 2.5s;"></i>
        </div>
        <div style="flex: 1; min-width: 0;">
          <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
            <h4 style="margin: 0; font-size: 0.925rem; font-weight: 600; color: #ffffff; letter-spacing: -0.01em;">Update Available</h4>
            <span style="font-size: 0.68rem; font-weight: 700; text-transform: uppercase; padding: 0.1rem 0.4rem; border-radius: 0.25rem; background: rgba(16, 185, 129, 0.25); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3);">New</span>
          </div>
          <p style="margin: 0 0 0.75rem 0; font-size: 0.8rem; line-height: 1.35; color: #cbd5e1;">
            A new feature or system update is ready. Click below to apply it.
          </p>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <button id="pwa-update-btn" style="cursor: pointer; border: none; outline: none; padding: 0.45rem 0.95rem; font-size: 0.8rem; font-weight: 600; border-radius: 0.5rem; background: #2563eb; color: #ffffff; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4); display: inline-flex; align-items: center; gap: 0.4rem; transition: background 0.2s, transform 0.1s;">
              <i class="fas fa-arrow-down-to-bracket"></i> Click to Update
            </button>
            <button id="pwa-later-btn" style="cursor: pointer; border: none; outline: none; padding: 0.45rem 0.75rem; font-size: 0.775rem; font-weight: 500; border-radius: 0.5rem; background: transparent; color: #94a3b8; transition: color 0.2s, background 0.2s;">
              Later
            </button>
          </div>
        </div>
        <button id="pwa-dismiss-btn" title="Dismiss" style="cursor: pointer; border: none; background: transparent; color: #64748b; font-size: 0.9rem; padding: 0.25rem; margin: -0.25rem -0.25rem 0 0; line-height: 1; transition: color 0.2s;">
          <i class="fas fa-times"></i>
        </button>
      </div>
    `;

    document.body.appendChild(toast);

    // Bind action events
    const updateBtn = document.getElementById('pwa-update-btn');
    const laterBtn = document.getElementById('pwa-later-btn');
    const dismissBtn = document.getElementById('pwa-dismiss-btn');

    if (updateBtn) {
      updateBtn.addEventListener('click', function() {
        if (isUpdating) return;
        isUpdating = true;
        updateBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Updating...';
        updateBtn.style.opacity = '0.85';
        updateBtn.style.pointerEvents = 'none';

        if (waitingWorker) {
          console.log('[PWA Updater] Sending SKIP_WAITING to waiting service worker...');
          waitingWorker.postMessage({ type: 'SKIP_WAITING' });
        } else if (swRegistration && swRegistration.waiting) {
          swRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });
        } else {
          // Fallback reload
          window.location.reload();
        }
      });

      // Hover styling
      updateBtn.addEventListener('mouseenter', () => updateBtn.style.background = '#1d4ed8');
      updateBtn.addEventListener('mouseleave', () => updateBtn.style.background = '#2563eb');
    }

    const hideToast = function() {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(1.5rem) scale(0.96)';
      toast.style.pointerEvents = 'none';
    };

    if (laterBtn) laterBtn.addEventListener('click', hideToast);
    if (dismissBtn) dismissBtn.addEventListener('click', hideToast);

    return toast;
  }

  // 2. Display the alert with smooth transition
  function showUpdatePrompt(worker) {
    waitingWorker = worker;
    updateToast = createUpdateToast();
    if (!updateToast) return;

    // Show toast
    setTimeout(() => {
      updateToast.style.opacity = '1';
      updateToast.style.transform = 'translateY(0) scale(1)';
      updateToast.style.pointerEvents = 'auto';
    }, 150);
  }

  // 3. Register Service Worker and attach lifecycle handlers
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then(function(registration) {
        swRegistration = registration;
        console.log('[PWA Updater] ServiceWorker registered with scope:', registration.scope);

        // Scenario A: Service Worker is already waiting (installed in background or previous tab)
        if (registration.waiting) {
          console.log('[PWA Updater] A new ServiceWorker is already waiting.');
          showUpdatePrompt(registration.waiting);
          return;
        }

        // Scenario B: An update is found during this session
        registration.addEventListener('updatefound', function() {
          const newWorker = registration.installing;
          console.log('[PWA Updater] New ServiceWorker found installing...');

          newWorker.addEventListener('statechange', function() {
            console.log('[PWA Updater] New ServiceWorker state changed to:', newWorker.state);
            // When worker has finished installing and there is an existing active controller
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              console.log('[PWA Updater] New version installed and waiting for activation!');
              showUpdatePrompt(newWorker);
            }
          });
        });

        // Background check: Check for updates every 15 minutes
        setInterval(function() {
          console.log('[PWA Updater] Checking for PWA updates in background...');
          registration.update().catch(err => console.warn('[PWA Updater] Update check failed:', err));
        }, 15 * 60 * 1000);

        // Foreground check: Check for updates when user returns to app
        document.addEventListener('visibilitychange', function() {
          if (document.visibilityState === 'visible') {
            console.log('[PWA Updater] App brought to foreground. Checking for updates...');
            registration.update().catch(err => console.warn('[PWA Updater] Foreground update check failed:', err));
          }
        });
      })
      .catch(function(error) {
        console.error('[PWA Updater] ServiceWorker registration failed:', error);
      });

    // 4. Reload page when the new Service Worker takes control
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', function() {
      if (refreshing) return;
      refreshing = true;
      console.log('[PWA Updater] Controller changed. Reloading page to apply updates...');
      window.location.reload();
    });
  });

})();
