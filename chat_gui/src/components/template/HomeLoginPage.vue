<template>
  <div class="home-login-container">
    <div class="container">
      <!-- header -->
      <h1>Welcome back</h1>
      <!-- userName & password -->
      <div class="form-group" v-if="!isUseTokenKey">
        <input v-model="userName" required />
        <label>User name*</label>
      </div>
      <div class="form-group" v-if="!isUseTokenKey">
        <input type="password" v-model="password" required />
        <label>Password*</label>
      </div>
      <!-- token key login -->
      <div class="form-group" v-if="isUseTokenKey">
        <input v-model="tokenKey" required />
        <label>tokenKey*</label>
      </div>
      <!-- login button -->
      <button @click="onLogin">Login</button>
      <!-- sign in -->
      <a>Don't have an account? <strong>Sign Up</strong></a>

      <div class="or"><span>OR</span></div>
      <!-- other options -->

      <div class="social-login">
        <!-- login with test user information -->
        <button @click="onRandomUserLogin">
          <div class="svg-icon" v-html="random24Icon"></div>
          Using a random test user
        </button>
        <!-- login in with token key -->
        <button @click="onLoginWithTokenKey">
          <div class="svg-icon" v-html="token24Icon"></div>
          {{ loginWithTokenButtonLabel }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { random24Icon, token24Icon } from "../../assets/styles/home/svgs.js";
export default {
  setup() {
    const isUseTokenKey = ref(false);
    const userName = ref("");
    const password = ref("");
    const tokenKey = ref("");
    const loginWithTokenButtonLabel = ref("Using a token key");
    onMounted(() => {});
    const onLogin = async () => {};
    const onLoginWithTokenKey = () => {
      if (isUseTokenKey.value) {
        // 改变文字
        loginWithTokenButtonLabel.value = "Using a token key";
        isUseTokenKey.value = false;
      } else {
        loginWithTokenButtonLabel.value = "Using username";
        isUseTokenKey.value = true;
      }
    };
    const onRandomUserLogin = () => {
      isUseTokenKey.value = false;
      userName.value = "Test" + (Math.floor(Math.random() * 100) + 1);
      password.value = "Test" + (Math.floor(Math.random() * 100) + 1);
      setTimeout(async function () {
        await onLogin();
      }, 1000);
    };
    return {
      isUseTokenKey,
      random24Icon,
      token24Icon,
      userName,
      password,
      tokenKey,
      loginWithTokenButtonLabel,
      onLogin,
      onLoginWithTokenKey,
      onRandomUserLogin,
    };
  },
};
</script>
