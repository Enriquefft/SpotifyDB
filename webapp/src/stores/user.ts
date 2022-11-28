import { defineStore } from "pinia";
import { ref } from "vue";
import type { Ref } from "vue";

function stringToArray(str: string | null): string[] {
  if (str === null) {
    return [];
  }
  return str.split(",");
}

interface data {
  username: string;
  access_token: string;
  remember_user?: boolean;
  isAuthorized?: boolean;
}

export const useUserStore = defineStore("user", () => {
  // Read remember_user
  const remember_user: Ref<boolean | undefined> = ref(undefined);
  const username: Ref<string | null> = ref(null);
  const isLoggedIn: Ref<boolean> = ref(true); // Ease of use function
  const isAuthorized: Ref<boolean> = ref(false); // Ease of use function
  const permits: Ref<string[]> = ref(["unlogged"]);
  const access_token: Ref<string | null> = ref(null);

  let a: string | null;
  if ((a = localStorage.getItem("remember_user")) !== null) {
    remember_user.value = a === "true";
  }

  switch (remember_user.value) {
    case true:
      username.value = localStorage.getItem("username");
      permits.value = stringToArray(localStorage.getItem("permits"));
      access_token.value = localStorage.getItem("access_token");
      isAuthorized.value = localStorage.getItem("isAuthorized") === "true";
      break;

    case false:
      username.value = sessionStorage.getItem("username");
      permits.value = stringToArray(sessionStorage.getItem("permits"));
      access_token.value = sessionStorage.getItem("access_token");
      isAuthorized.value = sessionStorage.getItem("isAuthorized") === "true";
      break;

    case undefined:
      isLoggedIn.value = false;
      break;
  }
  function login(data: data) {
    console.log(data);
    if (isLoggedIn.value) {
      throw "user is already logged in";
    }

    if (data.isAuthorized) {
      isAuthorized.value = true;
    }

    username.value = data.username;
    access_token.value = data.access_token;
    remember_user.value = data.remember_user;
    isLoggedIn.value = true;

    // Remove "unlogged" permit
    const i = permits.value.indexOf("unlogged");
    if (i >= 0) {
      permits.value.splice(i, 1);
    }

    switch (remember_user.value) {
      case true:
        localStorage.setItem("username", username.value);
        localStorage.setItem("permits", permits.value.join());
        localStorage.setItem("access_token", access_token.value);
        localStorage.setItem("remember_user", String(remember_user.value));
        localStorage.setItem("isAuthorized", String(isAuthorized.value));
        break;

      case false:
        sessionStorage.setItem("username", username.value);
        sessionStorage.setItem("permits", permits.value.join());
        sessionStorage.setItem("access_token", access_token.value);
        sessionStorage.setItem("remember_user", String(remember_user.value));
        sessionStorage.setItem("isAuthorized", String(isAuthorized.value));
        break;
    }
  }

  // logout
  function logout() {
    switch (remember_user.value) {
      case true:
        localStorage.clear();
        break;

      case false:
        sessionStorage.clear();
        break;

      default:
        throw "user is not logged int";
    }
    remember_user.value = undefined;
    username.value = null;
    isLoggedIn.value = false;
    permits.value = ["unlogged"];
    access_token.value = null;
    isAuthorized.value = false;
  }

  return {
    username,
    access_token,
    remember_user,
    isLoggedIn,
    isAuthorized,
    permits,
    login,
    logout,
  };
});
