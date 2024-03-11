<template>
  <div class="container">
    <div
      style="position: absolute; left: 10%; top: 20%; width: 80%; height: 60%"
    >
      <el-carousel :autoplay="false" :trigger="triggerType" type="card">
        <el-carousel-item v-for="item in cardList" :key="item">
          <h3 text="2xl" justify="center">{{ item.name }}</h3>
          <el-button
            @click="goPlayground(item)"
            :style="{
              width: '80%',
              height: '25%',
              margin: '10% 10% 10% 10%',
              display: 'flex',
              border: '1px black solid',
              'flex-direction': 'row',
              'align-items': 'center',
              'background-color': 'transparent',
              'border-radius': '20px',
            }"
          >
            <el-icon><Promotion /></el-icon>
            <el-text>Go</el-text>
          </el-button>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>
<script>
import { ref, onMounted, computed} from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
export default {
  setup() {
    const router = useRouter();
    const triggerType = ref("click");
    const cardList = ref([
      { name: "Azure Chat GPT", path: "/chat" },
      { name: "OpenAI Chat GPT", path: "/chat" },
    ]);
    const store = useStore();
    const loginState = computed(() => store.state.loginState);

    /** ====================== 下面定义函数 ====================== */
    onMounted(() => {
      if (!loginState.value) {
        ElMessage.error("请先登录！");
        // 回到登录界面
        router.push({
          path: "/",
        });
      }
    });
    
    const goPlayground = (val) => {
      if (val.name == "OpenAI Chat GPT") {
        ElMessage.info("Not Found The OpenAI GPT Key, 敬请期待！");
        return;
      }
      router.push({
        path: val.path,
      });
    };
    return {
      triggerType,
      cardList,
      goPlayground,
    };
  },
};
</script>
<style scoped>
.container {
  width: 100vw;
  height: 100vh;
}
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 100%;
  margin: 10% 0% 0% 0%;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}
</style>
