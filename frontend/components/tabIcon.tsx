import React from 'react'
import { StyleSheet, View, Text } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

type MaterialIconName = React.ComponentProps<typeof MaterialIcons>['name'];

interface TabIconProps {
  title: string;
  icon: MaterialIconName;
  focused: boolean;
}

const TabIcon: React.FC<TabIconProps> = ({ title, icon, focused }) => {
    return (
        <View style={[styles.container, { backgroundColor: focused ? 'rgba(0, 0, 0, 0.1)' : 'transparent' }]}>
            <MaterialIcons 
                name={icon} 
                size={24} 
                color={focused ? 'black' : 'gray'}
            />
            <Text
                style={[styles.text, { color: focused ? 'black' : 'gray' }]}>
                {title}
            </Text>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 4,
        borderRadius: 50
    },
    icon: {
        marginBottom: 4,
    },
    text: {
        fontSize: 10,
        fontWeight: '500'
    }
});

export default TabIcon;
