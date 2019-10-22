import React , { Component } from 'react';
import {TouchableOpacity, StyleSheet, FlatList, Button, Picker, TextInput, Text, View, Modal} from 'react-native';


export default class App extends React.Component {
   state = {
     price:'0.0',
     symbol: 'EURUSD',
     user:'ali',
     last_response:"",
     url:"http://88.99.109.36:5000/?key=ISA6444&",
     last_signals_text:"[]",
     signals:[],
     modalVisible:false,
     selected_symbol:"",
     selected_price:"",
     is_mql_active:'OK',
    }
   updateSymbol = (symbol) => {
      this.setState({ symbol: symbol })
   }
   updatePrice = (price) => {
        this.setState({ price: price })
    }
   is_price_valide = () => {
      price = this.state.price
      float_price = parseFloat(price)
      if (isNaN(float_price)) {
        return false
      }else{
        float_price = String(float_price)
        if (float_price.length  == price.length )
          {
            return true
          }else{
            return false
          }
      }
    }
   add_signal = () => {
      valide = this.is_price_valide()
      if (valide) {
        url = this.state.url + "action=add_signal&symbol="+this.state.symbol+"&price="+this.state.price
        response = this.add_signal_fetch(url)
      }else{
        alert('The price is invalide')
      }
    }
   send_server = () => {
     fetch('http://88.99.109.36:5000/?action=get_signals')
     .then(function(response) {
       response.text().then((text) => {alert('response is ' + text)})
     }, function(error) {
       alert('network error : check your connections please')
     })

      }
   update_signals = () => {
     url = this.state.url + "action=get_signals"
     this.update_signals_fetch(url)
   }
   export_signals_from_text = (string) => {
     symbols = []
     prices = []
     string = string.replace("[","")
     string = string.replace("]","")
     string = string.trim()
     _symbols = string.split("'")
     for (i=1;i<_symbols.length;i=i+2){
       symbols.push(_symbols[i])
     }
     _prices = string.split(",")
     for (i=1;i<_prices.length;i=i+2){
       prices.push(_prices[i].replace(')','').replace('}',''))
     }
     this.state.signals = []
     _signals = []
     for (i=0;i<symbols.length;i++){
       _signals.push({symbol:symbols[i].trim(),price:prices[i].trim()})
     }
     _signals.reverse()
     this.setState({
       signals:_signals
     })
   }
   remove_signal = (symbol,price) => {
     this.setState({selected_price:price,selected_symbol:symbol})
     this.setModalVisible(true)
   }
   async remove_signal_sure(symbol,price){
     this.setModalVisible(false)
     url = this.state.url + "action=remove_signal&symbol="+symbol+"&price="+price
     await fetch(url)
      .then((response) => {
         response.text()
             .then((text) => {
                 /** handling the text */
                 if (text == "OK") {
                   alert('the signal has been deleted successfully')
                   this.update_signals()
                 }else{
                   alert('Server error')
                 }
             })
             .catch((error) => {
               /** handling exception */
               alert("Server error")
             })
     })
     .catch((error) => {
       /** handling exception */
       alert('Network error')
     })
   }
   async update_signals_fetch(url) {
     await fetch(url)
        .then((response) => {
            response.text()
                .then((text) => {
                  this.state.last_signals_text = text
                  this.export_signals_from_text(text)
                })
                .catch((error) => {
                  this.update_signals()
                })
        })
        .catch((error) => {
          this.update_signals()
        })
   }
   async add_signal_fetch(url) {
     await fetch(url)
        .then((response) => {
            response.text()
                .then((text) => {
                    /** handling the text */
                    if (text == "OK") {
                      alert('the signal has been sent successfully')
                      this.update_signals()
                    }else{
                      alert('Server error')
                    }
                })
                .catch((error) => {
                  /** handling exception */
                  alert("Server error")
                })
        })
        .catch((error) => {
          /** handling exception */
          alert('Network error')
        })
   }
   async is_mql_active_in_server() {
     url = this.state.url + "action=is_mql_active"
     await fetch(url)
        .then((response) => {
            response.text()
                .then((text) => {
                    /** handling the text */
                    if (text == "True") {
                      this.setState({is_mql_active:"OK"})
                    }else{
                      this.setState({is_mql_active:"Broken"})
                    }
                })
                .catch((error) => {
                  /** handling exception */
                })
        })
        .catch((error) => {
          /** handling exception */
        })
   }
   componentWillMount(){
        this.update_signals()
        this.interval = setInterval(() => this.is_mql_active_in_server(), 5000);
    }
   setModalVisible = (visible) => {
     this.setState({modalVisible: visible});
   }
   render() {
      return (
      <View style={styles.whole}>
        <View style={styles.header} />
        <View style={styles.main} >
          <View style={styles_parts.above}>
            <View>
              <View style={styles.picker_style_container}>
               <Picker style={styles.picker_style} selectedValue = {this.state.symbol} onValueChange={this.updateSymbol}>
                  <Picker.Item label = "EUR/USD" value = "EURUSD" />
                  <Picker.Item label = "XAU/USD" value = "XAUUSD" />
               </Picker>
              </View>
              <TextInput style = {styles.input}
                underlineColorAndroid = "transparent"
                keyboardType = "numeric"
                placeholder = "Price"
                placeholderTextColor = "#9a73ef"
                autoCapitalize = "none"
                onChangeText = {this.updatePrice}/>
                <Button style = {styles.send_button}
                  title="Send"
                  color="#46AB4A"
                  onPress={this.add_signal}
                />
            </View>
          </View>
          <View style={styles_parts.bottom}>
            <Modal
            animationType="fade"
            transparent={true}
            visible={this.state.modalVisible}
            onRequestClose={() => {
              this.setModalVisible(false)
            }}>
              <View style={{flex:1}}>
               <View style={{flex:0.35}}></View>
                <View style={{flex:0.3,backgroundColor:"#F87698",justifyContent:"center",alignItems: 'center'}}>
                  <Text style={{fontSize:16}}> Are you sure about removing </Text>
                  <Text style={{fontSize:16}}>symbol : {this.state.selected_symbol}</Text>
                  <Text style={{fontSize:16}}>price : {this.state.selected_price}</Text>
                  <View style={{marginTop:20,flexDirection:"row"}}>
                    <Button title="              No                " color="red" onPress={() => this.setModalVisible(false)}/>
                    <Button title="              Yes               " color="green" onPress={() => this.remove_signal_sure(this.state.selected_symbol,this.state.selected_price)}/>
                  </View>
                </View>

               <View style={{flex:0.35}}></View>
              </View>


            </Modal>


          <View><Text></Text></View>
            <FlatList
              data={this.state.signals}
              renderItem={({ item }) =>
                    <View style={{flexDirection:'row'}}>
                      <Text style={styles.text_itself}>{item.symbol}           {item.price}</Text>
                      <TouchableOpacity style={{ height: 20,marginLeft:10,marginTop:3}} onPress={() => this.remove_signal(item.symbol,item.price)}>
                        <Text style={{width:90,fontSize:17,color:'red'}}>remove</Text>
                      </TouchableOpacity>
                    </View>
            }
            keyExtractor={(item, index) => index.toString()}
              />
          </View>
        </View>
        <View style={styles.footer}>
          <View style={{flexDirection:"row"}}><Text style={styles.server_statuse_text}>{this.state.is_mql_active}</Text></View>
        </View>
      </View>

      );
   }
}

const styles_parts = StyleSheet.create({
  above : {
    flex : 1,
    backgroundColor : 'white',
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomColor: '#D74200',
    borderBottomWidth: 1,
  },
  bottom : {
    flex : 2,
    backgroundColor : 'white',
    justifyContent: 'center',
    alignItems: 'center',
  }
});

const styles = StyleSheet.create({
  text_itself:{
    fontSize:19,
    marginBottom : 10,
    borderBottomColor : "#fc6d00",
    borderBottomWidth : 1,
  },
  right_empty:{
    flex:0.1,
    backgroundColor:'blue',
  },
  left_empty:{
    flex:0.1,
    backgroundColor:'blue',
  },
  list_text:{
    flex:1,
    flexDirection:"row",
    marginBottom:20,
    backgroundColor: "red",
  },
  send_button : {
    marginTop : 30,
    textAlign: 'center',
  },
  picker_style_container : {
    justifyContent: 'center',
    alignItems: 'center',
  },
  picker_style : {
    width : 190,
  },
  text_2 :{
    marginTop : 10,
  },
  input: {
    textAlign: 'center',
    marginBottom: 25,
    height: 40,
    width : 200,
    borderBottomColor: '#D74200',
    borderBottomWidth: 2,
   },
   whole : {
      flex : 1,
   },
   main: {
      flex: 20,
      backgroundColor: 'white',
   },
   header: {
     flex: 2,
     backgroundColor: '#D74200',
   },
   footer: {
     flex: 1.5,
     justifyContent:"center",
     alignItems:"center",
     backgroundColor: '#D74200',
   },
   text: {
      fontSize: 25,
      alignSelf: 'center',
      color: 'red'
   },
});
