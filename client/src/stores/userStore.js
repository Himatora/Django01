import { onBeforeMount ,ref} from "vue";
import axios from "axios";
import { defineStore } from "pinia";
const useUserStore=defineStore("UserStore",()=>{
    const isAuthenticated=ref(false);
    const username=ref("");
    const userId=ref();
    const isSuperUser = ref(false); 
    async function fetchUser() {
        const r=await axios.get("/api/user/info/");
        isAuthenticated.value=r.data.is_authenticated;
        username.value=r.data.username;
        userId.value=r.data.user_id;
        isSuperUser.value=r.data.is_superuser;
    }
    onBeforeMount(()=>[
        fetchUser()
    ])
    return {
        isAuthenticated,
        username,
        userId,
        isSuperUser
    };
})
export default useUserStore