<template>
  <div class="container">
    <div
      style="
        width: 90%;
        height: 20%;
        margin: 1% 5% 0% 5%;
        display: flex;
        justify-content: center;
      "
    >
      <el-text size="large">Welcome to GPT Playground</el-text>
    </div>
    <div class="login_item">
      <div class="login_item_icon">
        <el-icon><User /></el-icon>
      </div>
      <el-input v-model="user" class="login_item_text" />
    </div>
    <div class="login_item">
      <div class="login_item_icon">
        <el-icon><Lock /></el-icon>
      </div>
      <el-input type="password" v-model="password" class="login_item_text" />
    </div>
    <div
      style="
        width: 60%;
        height: 20%;
        margin: 1% 20% 0% 20%;
        display: flex;
        justify-content: center;
        align-items: center;
      "
    >
      <el-icon :style="{ width: '10%' }"><Opportunity /></el-icon>
      <el-text :style="{ width: '45%' }" truncated>Select Test User: </el-text>
      <el-select
        v-model="selectUser"
        :style="{ width: '45%' }"
        @change="selectTestUser"
      >
        <el-option
          v-for="item in userList"
          :key="item"
          :label="item.name"
          :value="item.name"
        />
      </el-select>
    </div>
    <el-button class="login_button" @click="login"> Login</el-button>
    <div class="login_help">
      <el-button class="login_help_button" :style="{ width: '40%' }"
        >Sign In
      </el-button>
      <el-button class="login_help_button" :style="{ width: '60%' }">
        Forget password?
      </el-button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
export default {
  setup() {
    const labelPosition = ref("right");
    const selectUser = ref("None");
    const user = ref("");
    const password = ref("");
    const userList = ref([
      { name: "None" },
      { name: "Test1" },
      { name: "Test2" },
      { name: "Test3" },
    ]);
    const router = useRouter();
    onMounted(() => {});
    const selectTestUser = () => {
      if (selectUser.value == "None") {
        user.value = "";
        password.value = "";
      } else {
        user.value = selectUser.value;
        password.value = selectUser.value;
      }
    };
    const login = () => {
      // 检验身份，进入界面

      // 如果为管理员，进入特殊界面
      if (user.value == "pldz") {
        // 用path传参会出现警告，所以没有传参，走store获取信息
        // https://blog.csdn.net/qq_43072786/article/details/121204960
        router.push({
          path: "/admin",
        });
      }
    };
    return {
      labelPosition,
      selectUser,
      user,
      userList,
      password,
      selectTestUser,
      login,
    };
  },
};
</script>

<style scoped>
.container {
  position: absolute;
  left: 35%;
  top: 35%;
  width: 30%;
  height: 30%;
  background-color: rgb(230, 255, 255);
  display: flex;
  flex-direction: column;
}

.login_item {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 60%;
  height: 20%;
  margin: 1% 20% 0% 20%;
}

.login_item .login_item_icon {
  width: 10%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login_item .login_item_text {
  height: 60%;
  width: 90%;
  color: black;
}

.login_button {
  width: 60%;
  height: 15%;
  margin: 2% 20% 0% 20%;
  background-color: #75ede7;
}

.login_help {
  width: 90%;
  height: 10%;
  margin: 3% 5% 0% 5%;
  display: flex;
  justify-content: center;
}

.login_help .login_help_button {
  background-color: transparent;
  border: none;
  height: 60%;
  margin: 0% 5% 0% 5%;
}
</style>
