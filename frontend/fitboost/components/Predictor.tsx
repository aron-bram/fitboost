import React, { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';

const ClassificationComponent = () => {
  const [inputText, setInputText] = useState('');
  const [labelText, setLabelText] = useState('');

  const handlePress = async () => {
    try {
      const response = await fetch('http://localhost:5001/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          "Access-Control-Allow-Origin": "localhost:5001"
        },
        body: JSON.stringify({ text: inputText }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data)
      setLabelText(data.category);
    } catch (error) {
      Alert.alert('Error', error.message);
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter text"
        value={inputText}
        onChangeText={setInputText}
      />
      <Button title="Submit" onPress={handlePress} />
      <Text style={styles.label}>{labelText}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 12,
    paddingHorizontal: 8,
    width: '80%',
    color: 'red'
  },
  label: {
    marginTop: 12,
    fontSize: 18,
    textAlign: 'center',
    color: "red"
  },
});

export default ClassificationComponent;
