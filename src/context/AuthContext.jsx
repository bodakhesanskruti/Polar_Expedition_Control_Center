import {createContext,useContext,useState} from 'react';
const AuthContext=createContext(null);
export function AuthProvider({children}){const [user,setUser]=useState({name:'Control Officer',role:'EXPEDITION_CONTROLLER'});return <AuthContext.Provider value={{user,setUser}}>{children}</AuthContext.Provider>}
export const useAuth=()=>useContext(AuthContext);
