import type {ChatBubbleModel} from "@/types/ChatBubbleModel";
import type {UserModel} from "@/types/UserModel";
import {emptyUser} from "@/types/UserModel";

export interface UIState {
    user: UserModel;
    messages: ChatBubbleModel[];
    isLoading: boolean;
}

export const initialState: UIState = {
    user: emptyUser,
    messages: [],
    isLoading: true
};