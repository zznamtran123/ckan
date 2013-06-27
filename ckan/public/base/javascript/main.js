// Global ckan namespace
this.ckan = this.ckan || {};

(function (ckan, $) {
  ckan.PRODUCTION = 'production';
  ckan.DEVELOPMENT = 'development';
  ckan.TESTING = 'testing';

  /* Initialises the CKAN JavaScript setting up environment variables and
   * loading localisations etc. Should be called once the page is ready.
   *
   * Examples
   *
   *   $(function () {
   *     ckan.initialize();
   *   });
   *
   * Returns nothing.
   */
  ckan.initialize = function () {
    var body = $('body'),
      locale = $('html').attr('lang'),
      location = window.location,
      root = location.protocol + '//' + location.host;

    function getRootFromData(key) {
      return (body.data(key) || root).replace(/\/$/, '');
    }

    ckan.SITE_ROOT   = getRootFromData('siteRoot');
    ckan.LOCALE_ROOT = getRootFromData('localeRoot');
    ckan.API_ROOT    = getRootFromData('apiRoot');

    // Load the localisations before instantiating the modules.
    ckan.sandbox().client.getLocaleData(locale).done(function (data) {
      ckan.i18n.load(data);
      ckan.module.initialize();
    });
  };

  /* Returns a full url for the current site with the provided path appended.
   *
   * path          - A path to append to the url (default: '/')
   * includeLocale - If true the current locale will be added to the page.
   *
   * Examples
   *
   *   var imageUrl = sandbox.url('/my-image.png');
   *   // => http://example.ckan.org/my-image.png
   *
   *   var imageUrl = sandbox.url('/my-image.png', true);
   *   // => http://example.ckan.org/en/my-image.png
   *
   *   var localeUrl = sandbox.url(true);
   *   // => http://example.ckan.org/en
   *
   * Returns a url string.
   */
  ckan.url = function (path, includeLocale) {
    if (typeof path === 'boolean') {
      includeLocale = path;
      path = null;
    }

    path = (path || '').replace(/^\//, '');

    var root = includeLocale ? ckan.LOCALE_ROOT : ckan.SITE_ROOT;
    return path ? root + '/' + path : root;
  };

  ckan.sandbox.extend({url: ckan.url});

  if (ckan.ENV !== ckan.TESTING) {
    $(function () {
      ckan.initialize();
    });
  }

  // Forces this to redraw in Internet Explorer 7
  // This is useful for when IE7 doesn't properly render parts of the page after
  // some dom manipulation has happened
  $.fn.ie7redraw = function () {
    if ($.browser.msie && $.browser.version === '7.0') {
      $(this).css('zoom', 1);
    }
  };

}(this.ckan, this.jQuery));
