import TabIcon from "@/components/tabIcon";
import { Tabs } from "expo-router";
import React from "react";
import { Pressable, type PressableStateCallbackType, type StyleProp, type ViewStyle } from "react-native";

const getTabButtonStyle = (
  styleProp: StyleProp<ViewStyle> | ((state: PressableStateCallbackType) => StyleProp<ViewStyle>),
  pressed: boolean
): StyleProp<ViewStyle> => {
  const baseStyle =
    typeof styleProp === "function" ? styleProp({ pressed } as PressableStateCallbackType) : styleProp;

  return [
    baseStyle,
    {
      transform: [{ scale: pressed ? 0.93 : 1 }],
      opacity: pressed ? 0.9 : 1,
    },
  ];
};

const Layout = () => {
  return (
    <Tabs
      screenOptions={{
        tabBarStyle: {
          backgroundColor: '#fff',
          borderTopWidth: 1,
          borderTopColor: '#e0e0e0',
          height: 80,
          paddingBottom: 8
        },
        tabBarActiveTintColor: 'black',
        tabBarInactiveTintColor: 'gray',
        tabBarButton: (props) => (
          <Pressable
            {...(props as any)}
            android_ripple={{ color: 'rgba(0, 0, 0, 0.12)', borderless: false }}
            style={({ pressed }) => getTabButtonStyle(props.style, pressed)}
          />
        ),
      }}
    >
      <Tabs.Screen 
        name="index" 
        options={{ 
          title: "Home",
          headerShown: false,
          tabBarIcon: ({ focused }) => (
            <TabIcon title="Home" icon="home" focused={focused} />
          ),
          tabBarLabel: () => null,
        }} 
      />
      <Tabs.Screen 
        name="scan" 
        options={{ 
          title: "Scan",
          headerShown: false,
          tabBarIcon: ({ focused }) => (
            <TabIcon title="Scan" icon="photo-camera" focused={focused} />
          ),
          tabBarLabel: () => null,
        }} 
      />
      <Tabs.Screen 
        name="profile" 
        options={{ 
          title: "Profile",
          headerShown: false,
          tabBarIcon: ({ focused }) => (
            <TabIcon title="Profile" icon="person" focused={focused} />
          ),
          tabBarLabel: () => null,
        }} 
      />
      <Tabs.Screen 
        name="about" 
        options={{ 
          title: "About",
          headerShown: false,
          tabBarIcon: ({ focused }) => (
            <TabIcon title="About" icon="info" focused={focused} />
          ),
          tabBarLabel: () => null,
        }} 
      />
    </Tabs>
  );
}

export default Layout;

