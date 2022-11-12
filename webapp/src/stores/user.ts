import { defineStore } from "pinia";
import { ref } from "vue";
import type { Ref } from "vue";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
function parseString(str: string | null): string[] | null {
  if (str === null) {
    return null;
  }
  return str.split(",");
}

interface data {
  username: string;
  acces_token: string;
  remember_user: boolean | undefined;
}

export const useUserStore = defineStore("user", () => {
  // Read remember_user
  const remember_user: Ref<boolean | null> = ref(null);
  const username: Ref<string | null> = ref(null);
  const logged_in: Ref<boolean> = ref(true); // Ease of use function
  //const permits: Ref<string[] | null> = ref(null);
  const acces_token: Ref<string | null> = ref(null);

  let a: string | null;
  if ((a = localStorage.getItem("remember_user")) !== null) {
    remember_user.value = a === "true";
  }

  switch (remember_user.value) {
    case true:
      username.value = localStorage.getItem("username");
      //permits.value = parseString(localStorage.getItem("permits"));
      acces_token.value = localStorage.getItem("acces_token");
      break;

    case false:
      username.value = sessionStorage.getItem("username");
      //permits.value = parseString(sessionStorage.getItem("permits"));
      acces_token.value = sessionStorage.getItem("acces_token");
      break;

    case null:
      logged_in.value = false;
      break;
  }
  function login(data: data) {
    console.log(data);
  }
  function register(data: data) {
    console.log(data);
  }
  return { username, acces_token, remember_user, logged_in, login, register };
});
