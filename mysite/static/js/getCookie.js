/**
 * Retrieves the value of a cookie by its name from the document's cookies.
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the specified cookie if found; otherwise, null.
 */
export default function getCookie(name) {
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}
