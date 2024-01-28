<template>
    <div class="container">
        <el-form :label-position="labelPosition" label-width="200px" :model="formLabelAlign" style="max-width: 460px">
            <el-form-item label="Model Type: ">
                <el-select v-model="model" style="width: 240px">
                    <el-option v-for="item in modelTypes" :key="item.value" :label="item.label" :value="item.value"
                        :disabled="item.disabled" />
                </el-select>
            </el-form-item>
            <el-form-item label="Chat Name: ">
                <el-input v-model="chatName" />
            </el-form-item>
            <el-form-item label="System Content: ">
                <el-input v-model="systemContent" />
            </el-form-item>
            <!-- 暂时不添加用户提问 -->
            <!-- <el-form-item label="User Content: ">
                <el-input v-model="userContent" />
            </el-form-item> -->
            <!-- 暂时不添加GPT的回答 -->
            <!-- <el-form-item label="Assistant Content: ">
                <el-input v-model="assistantContent" />
            </el-form-item> -->
            <el-checkbox style="margin-left: 300px" v-model="useDefault" @change="customPrompt">Use Default
                Prompt</el-checkbox>
        </el-form>
        <el-button @click="startChat" style="width:80%; margin-left: 50px">Start Chat</el-button>
    </div>
</template>
  
<script>
import { ref, onMounted } from "vue";
import { ElMessage } from 'element-plus'
import { postPrompt } from "../../apis/chatAPIs.js";
export default {
    name: "PromptCard",
    emits: ["startChat"],
    setup(props, context) {
        const labelPosition = ref('right');
        const model = ref('gpt4-32k')
        const modelTypes = ref([{value: 32 * 1024,label: 'gpt4-32k'}, { value: 16 * 1024, label: 'gpt4' }, { value: 32 * 1024, label: 'gpt3.5-32k-turbo' }])
        const chatName = ref('');
        const systemContent = ref('');
        const userContent = ref('');
        const assistantContent = ref('');
        const useDefault = ref(true);
        onMounted(() => {
            // 使用默认的prompt
            if (useDefault.value) {
                useDefaultPrompt();
            }
        });

        const padZero = (value) => {
            return String(value).padStart(2, '0');
        };

        const useDefaultPrompt = () => {

            const now = new Date();
            chatName.value = `${now.getFullYear()}-${padZero(now.getMonth() + 1)}-${padZero(now.getDate())}-${padZero(now.getHours())}-${padZero(now.getMinutes())}-${padZero(now.getSeconds())}`;
            systemContent.value = 'You are a helpful assistant.'
        }

        const customPrompt = () => {
            // 使用默认的prompt
            if (useDefault.value) {
                useDefaultPrompt();
            } else {
                chatName.value = '';
                systemContent.value = ''
            }
        }

        const startChat = async () => {
            const regex = /^[a-zA-Z0-9+-_]+$/;
            if (!regex.test(chatName.value)) {
                ElMessage.error('必须给对话起合适的名称(字母/数字/下划线/+-符号组成)')
                context.emit("startChat", {name: '', rea: false, num: 0});
            }
            var allTokens = modelTypes.value.find(type => type.label === model.value);  
            await postPrompt({name: chatName.value, msg: systemContent.value})
            context.emit("startChat", {name: chatName.value, rea: true, num: allTokens.value});
        }

        return {
            labelPosition,
            model,
            modelTypes,
            chatName,
            systemContent,
            userContent,
            assistantContent,
            useDefault,
            customPrompt,
            startChat,
        };
    },
};
</script>
  
<style scoped>
.container {
    display: flex;
    width: 100%;
    height: 100%;
    flex-direction: column;
    padding: 15px 0px 0px 0px;
}
</style>
  