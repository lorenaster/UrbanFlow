import React, { useEffect, useState } from "react";
import { View, Text } from "react-native";
import axios from "axios";

export default function Test() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get("http://192.168.0.153:8000/api/hello/")
      .then(response => setMessage(response.data.message))
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>{message}</Text>
    </View>
  );
}
