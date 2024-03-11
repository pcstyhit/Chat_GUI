import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../components/home/LoginPage.vue";
import AdminPage from "../components/home/AdminPage.vue";
import PlaygroundPage from "../components/home/PlaygroundCard.vue";
import ChatPage from "../components/chat/HomePage.vue";
import ElementHomeEmpty from "../components/template/HomeEmptyPage.vue";
import ElementHomeLogin from "../components/template/HomeLoginPage.vue";
import ElementHomeAdmin from "../components/template/HomeAdminPage.vue";
import ElementChatDrawer from "../components/template/ChatDrawerCard.vue";
import ElementChatPrompt from "../components/template/ChatPromptCard.vue";
import ElementChatChat from "../components/template/ChatChatCard.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      // 默认打开跳转路由
      // https://juejin.cn/post/7195183916481773624
      path: "/",
      redirect: "/login",
    },
    {
      path: "/login",
      component: LoginPage,
    },
    {
      path: "/admin",
      component: AdminPage,
    },
    {
      path: "/playground",
      component: PlaygroundPage,
    },
    {
      path: "/chat",
      component: ChatPage,
    },
    {
      path: "/template/home/empty",
      component: ElementHomeEmpty,
    },
    {
      path: "/template/home/login",
      component: ElementHomeLogin,
    },
    {
      path: "/template/home/admin",
      component: ElementHomeAdmin,
    },
    {
      path: "/template/chat/drawer",
      component: ElementChatDrawer,
    },
    {
      path: "/template/chat/prompt",
      component: ElementChatPrompt,
    },
    {
      path: "/template/chat/chat",
      component: ElementChatChat,
    },
  ],
});
export default router;
