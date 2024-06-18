<template>
  <div class="home-login-container">
    <div class="container" v-loading="isLoading">
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
      <a @click.prevent="onToDoButton"
        >Don't have an account? <strong>Sign Up</strong></a
      >

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
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { logIN } from "../../apis/login.js";
import { random24Icon, token24Icon } from "../../assets/styles/home/svgs.js";
export default {
  setup() {
    const router = useRouter();
    const store = useStore();

    const userName = ref("");
    const password = ref("");
    const tokenKey = ref("");
    const isUseTokenKey = ref(false);
    const loginWithTokenButtonLabel = ref("Using a token key");
    const isLoading = ref(false);

    /** ====================== 下面定义函数 ====================== */
    onMounted(() => {
      store.commit("SET_LOGIN_STATE", false);
    });

    /** 判断用户身份然后登录到应用中，并存入全局的身份信息. */
    const onLogin = async () => {
      // 限制操作
      isLoading.value = true;
      // 存入登录信息，用于HTTP Request获取内容
      store.commit("SET_USER_NAME", userName.value);
      store.commit("SET_BASIC_AUTH", generateBasicAuth());
      // 检验身份，进入界面
      var rea = await logIN();
      // 登录成功
      if (rea.flag) {
        store.commit("SET_LOGIN_STATE", true);
        // 用path传参会出现警告，所以没有传参，走store获取信息
        // https://blog.csdn.net/qq_43072786/article/details/121204960
        router.push({
          path: userName.value == "admin" ? "/admin" : "/chat",
        });
      } else {
        ElMessage.info(rea.msg);
      }
      isLoading.value = false;
    };

    /** 生成Basic Auth认证的header */
    const generateBasicAuth = () => {
      return "Basic " + btoa(userName.value + ":" + password.value);
    };

    const onLoginWithTokenKey = () => {
      if (isUseTokenKey.value) {
        // 改变文字
        loginWithTokenButtonLabel.value = "Using a token key";
        isUseTokenKey.value = false;
      } else {
        onToDoButton();
        loginWithTokenButtonLabel.value = "Using username";
        isUseTokenKey.value = true;
      }
    };

    const onRandomUserLogin = () => {
      isUseTokenKey.value = false;
      userName.value = "Test" + (Math.floor(Math.random() * 100) + 1);
      password.value = userName.value;
      setTimeout(async function () {
        await onLogin();
      }, 500);
    };

    const onToDoButton = () => {
      ElMessage.info("敬请期待 😋");
    };

    return {
      isUseTokenKey,
      random24Icon,
      token24Icon,
      userName,
      password,
      tokenKey,
      loginWithTokenButtonLabel,
      isLoading,
      onLogin,
      onLoginWithTokenKey,
      onRandomUserLogin,
      onToDoButton,
    };
  },
};
</script>
