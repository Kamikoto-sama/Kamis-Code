package com.example.testapp

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    fun toastMe(view: View){
        val myToast = Toast.makeText(this, "Text message", Toast.LENGTH_SHORT)
        myToast.show()
    }

    fun countMe(view: View){
        var currentCount = count.text.toString()
        var newCount: Int = Integer.parseInt(currentCount)
        newCount++
        count.text = newCount.toString()
    }
}
